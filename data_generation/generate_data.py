# To run this script, you first need to install the 'Faker' library:
# pip3 install Faker

import csv
import random
import uuid
import string
from datetime import datetime, timedelta
from faker import Faker
from collections import defaultdict

# --- CONFIGURATION ---

EVENT_DEFINITIONS = {
    'tamper': {
        'initiating': ['EV_PID_STRAP_TAMPER_START'],
        'closing': ['EV_PID_STRAP_TAMPER_END'],
        'threshold_minutes': 2
    },
    'curfew': {
        'initiating': [
            'EV_ZONE_INCLUSION_TU_ABSENT_AT_START_TIME',
            'EV_CURFEWED_PID_ABSENT',
            'EV_PID_ABSENT',
            'EV_PID_ABSENT_DURING'
        ],
        'closing': [
            'EV_ZONE_INCLUSION_TU_ARRIVED_DURING_TIME',
            'EV_CURFEWED_PID_ARRIVED',
            'EV_PID_ARRIVED'
        ],
        'threshold_minutes': 10
    },
    'exclusion': {
        'initiating': [
            'EV_EXCLUDED_PID_ARRIVED_DURING_EXCLUSION',
            'EV_ZONE_EXCLUSION_TU_PRESENT_AT_START_TIME',
            'EV_ZONE_EXCLUSION_TU_ARRIVED_DURING_TIME'
        ],
        'closing': [
            'EV_EXCLUDED_PID_DEPARTED_DURING_EXCLUSION',
            'EV_ZONE_EXCLUSION_TU_DEPARTED_DURING_TIME'
        ],
        'threshold_minutes': 5
    },
    'battery': {
        'initiating': [
            'EV_ENTER_LOW_POWER_STATE',
            'EV_PID_BATTERY_LOW',
            'EV_BATTERY_LEV_5PERCENT'
        ],
        'closing': [
            'EV_CHARGING_STARTED',
            'EV_MU_MAINS_START'
        ],
        'threshold_minutes': 2
    }
}

# --- HELPER FUNCTIONS ---

def get_user_input(prompt, input_type=int, min_val=0, max_val=None):
    """Generic function to get and validate user input."""
    while True:
        try:
            value = input_type(input(prompt))
            if value < min_val:
                print(f"  ❌ Error: Value must be at least {min_val}.")
            elif max_val is not None and value > max_val:
                print(f"  ❌ Error: Value must be no more than {max_val}.")
            else:
                return value
        except ValueError:
            print(f"  ❌ Error: Invalid input. Please enter a valid {input_type.__name__}.")

def get_parameters():
    """Prompts the user for all necessary script parameters."""
    print("📋 Please provide the following parameters for data generation:")
    
    params = {}
    params['num_persons'] = get_user_input("1. Number of person records to generate: ", min_val=1)
    
    max_threshold = max(d['threshold_minutes'] for d in EVENT_DEFINITIONS.values())
    print(f"   (Note: Minimum event span is {max_threshold} minutes to accommodate event thresholds)")
    params['event_span_minutes'] = get_user_input(f"2. Span of time for events (in minutes): ", min_val=max_threshold)
    
    params['no_events_perc'] = get_user_input("3. Percentage of persons with NO events (0-100): ", input_type=float, min_val=0, max_val=100)
    
    print("\nℹ️ The following percentages are based on the subset of people who HAVE events.")
    for category in EVENT_DEFINITIONS.keys():
        print(f"\n--- {category.capitalize()} Event Configuration ---")
        prompt_text = f"Percentage of event-having persons with initiating '{category}' events (0-100): "
        params[f'{category}_perc'] = get_user_input(prompt_text, input_type=float, min_val=0, max_val=100)
        
        while True:
            within_thresh_perc = get_user_input(f"  -> Percentage of these that close WITHIN threshold (0-100): ", input_type=float, min_val=0, max_val=100)
            outside_thresh_perc = get_user_input(f"  -> Percentage of these that close OUTSIDE threshold (0-100): ", input_type=float, min_val=0, max_val=100)
            
            if within_thresh_perc + outside_thresh_perc <= 100:
                params[f'{category}_within_thresh_perc'] = within_thresh_perc
                params[f'{category}_outside_thresh_perc'] = outside_thresh_perc
                break
            else:
                print("  ❌ Error: The sum of 'within' and 'outside' threshold percentages cannot exceed 100. Please try again.")
                
    return params

def format_timestamp(ts):
    """Formats a datetime object to YYYY-MM-DDThh:mm:ss.SSSS string."""
    return ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-2]

def sanitize_timestamp_for_filename(ts_str):
    """Replaces characters in a timestamp string that are invalid in filenames."""
    return ts_str.replace(":", "_")

# --- DATA GENERATION FUNCTIONS ---

def generate_persons_data(num_persons):
    """Generates a list of synthetic person records and their shared timestamp."""
    print("\nGenerating person data...")
    fake = Faker('en_GB')
    persons = []
    
    base_time = datetime.now() - timedelta(hours=random.randint(49, 100), minutes=random.randint(0, 59))
    person_timestamp_str = format_timestamp(base_time)

    for i in range(1, num_persons + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        person = {
            'id': i,
            'delius_id': f"{random.choice(string.ascii_uppercase)}{random.randint(100000, 999999)}",
            'unique_device_wearer_id': f"DEVW{random.randint(1000000, 9999999)}",
            'person_id': uuid.uuid4().hex,
            'given_name': first_name,
            'family_name': last_name,
            'alias': first_name[:3].lower() + last_name[:2].lower() if random.choice([True, False]) else '',
            'timestamp': person_timestamp_str,
            'toy': 'False'
        }
        persons.append(person)
    print(f"✅ Generated {len(persons)} person records.")
    return persons, person_timestamp_str

def _create_event_pair(person_id, category, params, event_start_time, event_end_time):
    """Helper to create an initiating event and a potential closing event."""
    details = EVENT_DEFINITIONS[category]
    events = []

    # Create the initiating event
    init_event_time_delta = timedelta(minutes=random.uniform(0, params['event_span_minutes']))
    init_timestamp = event_start_time + init_event_time_delta
    
    initiating_event = {
        'person_id': person_id,
        'event_name': random.choice(details['initiating']),
        'timestamp': format_timestamp(init_timestamp)
    }
    events.append(initiating_event)

    # Decide if a closing event should be generated
    rand_val = random.uniform(0, 100)
    close_timestamp = None

    if rand_val < params[f'{category}_within_thresh_perc']:
        # Enforce a minimum of 60 seconds between initiating and closing events.
        # All thresholds are >= 2 minutes, so this is safe.
        lower_bound_seconds = 60
        upper_bound_seconds = details['threshold_minutes'] * 60
        time_delta_seconds = random.uniform(lower_bound_seconds, upper_bound_seconds)
        close_timestamp = init_timestamp + timedelta(seconds=time_delta_seconds)

    elif rand_val < (params[f'{category}_within_thresh_perc'] + params[f'{category}_outside_thresh_perc']):
        # This case is already guaranteed to be > 60 seconds as all thresholds are >= 2 minutes.
        min_delta = details['threshold_minutes'] * 60 + 1
        max_delta = (event_end_time - init_timestamp).total_seconds()
        if max_delta > min_delta:
            time_delta_seconds = random.uniform(min_delta, max_delta)
            close_timestamp = init_timestamp + timedelta(seconds=time_delta_seconds)
    
    if close_timestamp:
        closing_event = {
            'person_id': person_id,
            'event_name': random.choice(details['closing']),
            'timestamp': format_timestamp(close_timestamp)
        }
        events.append(closing_event)
        
    return events


def generate_events_data(persons, params, event_start_time):
    """Generates a list of synthetic event records based on user parameters."""
    print("Generating event data...")
    all_events = []
    
    event_end_time = event_start_time + timedelta(minutes=params['event_span_minutes'])

    # 1. Determine which persons will have events
    person_ids = [p['person_id'] for p in persons]
    num_with_events = int(len(person_ids) * (1 - params['no_events_perc'] / 100.0))
    persons_with_events_ids = random.sample(person_ids, k=num_with_events)
    
    if not persons_with_events_ids:
        print("⚠️ No persons selected to have events based on input percentages.")
        return []

    print(f"ℹ️  {len(persons_with_events_ids)} persons were selected to have events.")

    # Prepare for the weighted choice fallback
    categories = list(EVENT_DEFINITIONS.keys())
    weights = [params[f'{cat}_perc'] for cat in categories]
    
    # 2. Iterate through each person who MUST have an event
    for person_id in persons_with_events_ids:
        assigned_categories = []
        
        # 3. Use percentages as probabilities to assign event types
        for category in categories:
            if random.uniform(0, 100) < params[f'{category}_perc']:
                assigned_categories.append(category)
        
        # 4. GUARANTEE: If no event type was assigned by chance, force one
        if not assigned_categories:
            if sum(weights) > 0:
                chosen_category = random.choices(categories, weights=weights, k=1)[0]
                assigned_categories.append(chosen_category)
            else: 
                assigned_categories.append(random.choice(categories))
        
        # 5. Create the actual event records for the assigned types
        for category in assigned_categories:
            event_pair = _create_event_pair(person_id, category, params, event_start_time, event_end_time)
            all_events.extend(event_pair)

    # Finalize: Sort by time and re-assign sequential IDs
    all_events.sort(key=lambda x: x['timestamp'])
    for i, event in enumerate(all_events):
        event['id'] = i + 1

    print(f"✅ Generated {len(all_events)} event records.")
    return all_events


# --- FILE WRITING FUNCTIONS ---

def write_to_csv(filename, data, headers):
    """Writes a list of dictionaries to a single CSV file."""
    if not data:
        print(f"   - Skipping {filename} (no data for this chunk).")
        return
        
    print(f"   - Writing {len(data)} records to {filename}...")
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        print(f"❌ Error writing to file {filename}: {e}")

def write_chunked_event_csvs(events, event_start_time):
    """Groups events into 5-minute chunks and writes them to separate files."""
    if not events:
        print("⚠️ No event data to write.")
        return

    print("Chunking and writing event files...")
    event_headers = ['id', 'person_id', 'event_name', 'timestamp']
    
    chunked_events = defaultdict(list)
    chunk_interval_minutes = 5
    
    for event in events:
        event_ts_str = event['timestamp']
        event_dt = datetime.strptime(event_ts_str, '%Y-%m-%dT%H:%M:%S.%f')
        
        minutes_from_start = (event_dt - event_start_time).total_seconds() / 60
        chunk_index = int(minutes_from_start // chunk_interval_minutes)
        
        chunk_end_time = event_start_time + timedelta(minutes=(chunk_index + 1) * chunk_interval_minutes)
        chunked_events[chunk_end_time].append(event)
        
    for chunk_end_time, events_in_chunk in sorted(chunked_events.items()):
        ts_for_filename = sanitize_timestamp_for_filename(format_timestamp(chunk_end_time))
        filename = f"event-{ts_for_filename}.csv"
        write_to_csv(filename, events_in_chunk, event_headers)
    
    print("✅ Finished writing event files.")


# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # 1. Get parameters from the user
    script_params = get_parameters()

    # 2. Generate data in memory
    persons_data, person_timestamp = generate_persons_data(script_params['num_persons'])
    
    event_start_time = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    events_data = generate_events_data(persons_data, script_params, event_start_time)

    # 3. Write data to CSV files
    print("\nWriting data to CSV files...")
    if persons_data:
        sanitized_ts = sanitize_timestamp_for_filename(person_timestamp)
        person_filename = f"person-{sanitized_ts}.csv"
        person_headers = ['id', 'delius_id', 'unique_device_wearer_id', 'person_id', 'given_name', 'family_name', 'alias', 'timestamp', 'toy']
        print(f"Writing person data to {person_filename}...")
        write_to_csv(person_filename, persons_data, person_headers)
        print(f"✅ Successfully wrote {person_filename}.")

    write_chunked_event_csvs(events_data, event_start_time)
    
    print("\n🎉 Script finished.")