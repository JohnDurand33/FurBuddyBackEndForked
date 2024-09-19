# from database import db
# from datetime import datetime, timedelta
# from models.event import Event
# from models.schemas.eventSchema import event_schema, events_schema


# def create_event(current_owner_id, data):
#     event = event_schema.load(data)
#     event.owner_id = current_owner_id
#     db.session.add(event)
#     db.session.commit()
#     return event_schema.dump(event)


# def get_event(current_owner_id, event_id):
#     event = Event.query.get(id)
#     if event.owner_id != current_owner_id:
#         return None
#     return event_schema.dump(event)


# def update_event(current_owner_id, event_id, data):
#     event = Event.query.get(event_id)
#     if event.owner_id != current_owner_id:
#         return None
    
#     for key, value in data.items():
#         setattr(event, key, value)
#     db.session.commit()
#     return event_schema.dump(event)


# def delete_event(current_owner_id, event_id):
#     event = Event.query.get(event_id)
#     if event.owner_id != current_owner_id:
#         return None
    
#     db.session.delete(event)
#     db.session.commit()
#     return {"message": "Event deleted"}


# def get_events_for_day(date, current_owner_id):
#     start_of_day = datetime.combine(date, datetime.min.time())
#     end_of_day = start_of_day + timedelta(days=1)
#     events = Event.query.filter(
#         Event.start_time >= start_of_day,
#         Event.start_time < end_of_day,
#         Event.owner_id == current_owner_id
#     ).all()
#     return events_schema.dump(events)


# def get_events_for_week(start_date, current_owner_id):
#     start_of_week = start_date - timedelta(days=start_date.weekday())
#     end_of_week = start_of_week + timedelta(days=7)
#     events = Event.query.filter(
#         Event.start_time >= start_of_week,
#         Event.start_time < end_of_week,
#         Event.owner_id == current_owner_id
#     ).all()
#     return events_schema.dump(events)


# def get_events_for_month(year, month, current_owner_id):
#     start_of_month = datetime(year, month, 1)
#     end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)
#     events = Event.query.filter(
#         Event.start_time >= start_of_month,
#         Event.start_time < end_of_month,
#         Event.owner_id == current_owner_id
#     ).all()
#     return events_schema.dump(events)


# def get_all_events(view_type, start_date_str, year, month, current_owner_id):
#     if view_type == 'day':
#         date = datetime.strptime(start_date_str, '%Y-%m-%d')
#         return get_events_for_day(date, current_owner_id)
#     elif view_type == 'week':
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
#         return get_events_for_week(start_date, current_owner_id)
#     elif view_type == 'month':
#         year = int(year)
#         month = int(month)
#         return get_events_for_month(year, month, current_owner_id)
#     else:
#         raise ValueError("Invalid view type")