from repository.event_repository import EventRepository
from service.collaborative_filtering import predictSport, predictMusical, predictNature, predictStagePlay

def make_recommendation(event_type, user_id):
    try:
        if event_type == 'Sport':
            dataset = EventRepository().getSportEventRatesUser(user_id)
            return predictSport(dataset=dataset)
        if event_type == 'Musical':
            dataset = EventRepository().getMusicalEventRatesUser(user_id)
            return predictMusical(dataset=dataset)
        if event_type == 'Nature':
            dataset = EventRepository().getNatureEventRatesUser(user_id)
            return predictNature(dataset=dataset)
        if event_type == 'StagePlay':
            dataset = EventRepository().getStagePlayEventRatesUser(user_id)
            return predictStagePlay(dataset=dataset)
        
    except:
        if event_type == 'Sport':
            dataset = EventRepository().getSportEventRates()
            return predictSport(dataset=dataset)
        if event_type == 'Musical':
            dataset = EventRepository().getMusicalEventRates()
            return predictMusical(dataset=dataset)
        if event_type == 'Nature':
            dataset = EventRepository().getNatureEventRates()
            return predictNature(dataset=dataset)
        if event_type == 'StagePlay':
            dataset = EventRepository().getStagePlayEventRates()
            return predictStagePlay(dataset=dataset)
