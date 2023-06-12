from repository.event_repository import EventRepository
from service.content_based import predictSport, predictMusical, predictNature, predictStagePlay

def make_group_recommendation(event_type, user_ids):
    try:
        if event_type == 'Sport':
            dataset = EventRepository().getSportEventRatesUser(user_ids)
            return predictSport(dataset=dataset)
    except:
        if event_type == 'Sport':
            dataset = EventRepository().getSportEventRates()
            return predictSport(dataset=dataset)
        
    try:
        if event_type == 'Musical':
            dataset = EventRepository().getMusicalEventRatesUser(user_ids)
            return predictMusical(dataset=dataset)
    except:
        if event_type == 'Musical':
            dataset = EventRepository().getMusicalEventRates()
            return predictMusical(dataset=dataset)
    
    try:
        if event_type == 'Nature':
            dataset = EventRepository().getNatureEventRatesUser(user_ids)
            return predictNature(dataset=dataset)
    except:
        if event_type == 'Nature':
            dataset = EventRepository().getNatureEventRates()
            return predictNature(dataset=dataset)
    
    try:
        if event_type == 'StagePlay':
            dataset = EventRepository().getStagePlayEventRatesUser(user_ids)
            return predictStagePlay(dataset=dataset)
    except:
        if event_type == 'StagePlay':
            dataset = EventRepository().getStagePlayEventRates()
            return predictStagePlay(dataset=dataset)