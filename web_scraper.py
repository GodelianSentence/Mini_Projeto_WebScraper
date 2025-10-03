import requests
import time
import pandas as pd

def get_steam_reviews(appid, n_reviews=1000, language='brazilian'):
    
    API_URL = f"https://store.steampowered.com/appreviews/{appid}"
    
    params = {
        'json': 1,               
        'filter': 'all',         
        'language': language,    
        'num_per_page': 100,    
        'cursor': '*'            
    }

    reviews = []
    
    while len(reviews) < n_reviews:
        print(f"Coletando {len(reviews)} de {n_reviews} avaliações...")
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status() 
            data = response.json()
            
            batch_reviews = data['reviews']
            
            if not batch_reviews:
                print("Não há mais avaliações para coletar. Encerrando.")
                break
            
            for review in batch_reviews:
                reviews.append({
                    'review_id': review['recommendationid'],
                    'steam_id': review['author']['steamid'],
                    'review_text': review['review'],
                    'voted_up': review['voted_up'], 
                    'playtime_forever': review['author']['playtime_forever']
                })
            
            params['cursor'] = data['cursor']
            
            time.sleep(2) 
            
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            break
            
    return reviews

if __name__ == '__main__':
    app_id_death_stranding = 1190460
    
    reviews_data = get_steam_reviews(app_id_death_stranding, n_reviews=2000)

    if reviews_data:
        print(f"\nTotal de avaliações coletadas: {len(reviews_data)}")
        df = pd.DataFrame(reviews_data)
        
        filename = 'avaliacoes_death_stranding_steam.csv'
        df.to_csv(filename, index=False)
        print(f"Dados salvos em '{filename}'")
        
        print("\nExemplo das primeiras 5 avaliações:")
        print(df.head())
    else:
        print("\nNão foi possível coletar as avaliações.")
