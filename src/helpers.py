chiffre_dict = {
    'une': 1,
    'deux': 2,
    'trois': 3,
    'quatre': 4,
    'cinq': 5,
    'six': 6,
    'sept': 7,
    'huit': 8,
    'neuf': 9,
    'dix': 10,
}

def is_float(*strings):
    for string in strings:
        if string.replace(".", "").replace(",", "").isnumeric():
            pass
        else:
            return False
    return True

def trunc_after_term(str, term):
    return str[:str.index(term) + len(term)]

def convert_float(num_str):
    if num_str == '000': return num_str
    return round(float(num_str.replace(',','.')))

def findIndex_in_array(arr, term):
    for index, value in enumerate(arr):
        if term in value: return index
    return -1

def extract_house_feature(data, term):
    arrData = data.split(' ')
    index = findIndex_in_array(arrData, term)
    if index < 0: return ''
    if index == 0: return arrData[index]
    if (index > 1 and is_float(arrData[index-2], arrData[index-1]) and term == '€'):
        return f'{convert_float(arrData[index-2])} {convert_float(arrData[index-1])} {trunc_after_term(arrData[index], term)}'
    if is_float(arrData[index-1]): return f'{convert_float(arrData[index-1])} {trunc_after_term(arrData[index], term)}'
    if arrData[index-1] in chiffre_dict: return f'{chiffre_dict[arrData[index-1]]} {arrData[index]}'
    if term == '€': return arrData[index]
    if is_float(arrData[index][:-2]): return arrData[index]
    return ''
    

def find_in_array(arr, *terms):
    for term in terms:
        filtered_arr = list(filter(lambda x: term in x, arr))
        if len(filtered_arr): return extract_house_feature(filtered_arr[0], term)
    return ''

def prepare_data(data):
    data = data.replace('', '€')
    arr = data.split('\n')
    cleaned_arr = [tag.lower() for tag in arr]
    for i, el in enumerate(cleaned_arr):
        if el == 'm': cleaned_arr[i] = 'm2'
    cleaned_arr = [' '.join(cleaned_arr)]
    return cleaned_arr

def get_text_data(data):
    cleaned_arr = prepare_data(data)
    price = find_in_array(cleaned_arr, '€')
    surface = find_in_array(cleaned_arr, 'm²', 'm2')
    room = find_in_array(cleaned_arr, 'pièce')
    bedrooms = find_in_array(cleaned_arr, 'chambre')
    return price, surface, room, bedrooms

def return_csv_line(house):
    return ','.join(list(house.values()))

def append_csv(house_data, filename='unknown'):
    csv_filepath = f'./tmp/{filename}_scrape.csv'
    csv_data = list(map((lambda x: return_csv_line(x)), house_data))  
    with open(csv_filepath, 'a') as file:
         file.write('\n'.join(csv_data) + '\n')

def decode_str(str):
    string_encode = str.replace('', '€').replace('€', '$').encode('ascii', "ignore")
    return string_encode.decode().replace('$','€')

def _serialize_html(html, filePath):
    with open(filePath, 'w') as file:
        file.write(html)

def _get_local_html(filePath):
    with open(filePath, 'r') as file:
        html = file.read()
    return html

if __name__ == "__main__":
    
    test = '''
EXCLUSIVITE
VERNON
PROCHE COMMERCE ET GARE A PIED
IDEAL INVESTISSEUR
MAISON DE VILLE DE 64 M2 AVEC COURETTE A RENOVER DANS SON ENSEMBLE comprenant :
Au rez-de-chaussée : cuisine de 19 m2, séjour de 21 m2 avec cheminée.
A létage : 2 chambres, salle de bains ...
Plus d'informations
Vernon
108 000 
    '''

    print(get_text_data(test))