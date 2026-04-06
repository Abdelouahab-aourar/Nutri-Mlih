from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
def scrape():
    urls = [
        {"url": "https://areej.store/categorie-produit/market/pates-et-couscous-fr/", "category": "Pâtes et Couscous"},
        {"url": "https://areej.store/categorie-produit/market/pates-et-couscous-fr/page/2/", "category": "Pâtes et Couscous"},
        {"url": "https://areej.store/categorie-produit/market/produits-laitiers/", "category": "Produits Laitiers"},
        {"url": "https://areej.store/categorie-produit/market/legumes-secs/", "category": "Légumes Secs"},
        {"url": "https://areej.store/categorie-produit/market/cafes-et-sucres/", "category": "Cafés et Sucres"},
        {"url": "https://areej.store/categorie-produit/market/conserves-fr/", "category": "Conserves"},
        {"url": "https://areej.store/categorie-produit/market/boisson/", "category": "Boisson"},
        {"url": "https://areej.store/categorie-produit/market/huiles-vinaigre/", "category": "Huiles et Vinaigre"},
        {"url": "https://areej.store/categorie-produit/market/epicerie-sucree/", "category": "Epicerie-Sucree"}    
        ]
    data = []
    for item in urls:
        url = item["url"]
        category = item["category"]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        products_container = soup.find("div", class_="products")
        products = products_container.find_all("div", class_="product-small")
        for product in products:
            box = product.find("div", class_="box-text")
            name = box.find("div", class_="title-wrapper")
            if name:
                name = name.find("a")
                name = name.text.strip() if name else None
            price = box.find("div", class_="price-wrapper")
            if price:
                price = price.find("bdi")
                price = price.text.strip() if price else None
            data.append({
                "Name": name,
                "Price": price,
                "Category": category
            })
            time.sleep(0.1)
    df = pd.DataFrame(data)
    df.to_csv("data/products1.csv", index=False, encoding="utf-8-sig")
    print("Data 1 Saved Successfully")
    data = []
    urls = [
        {"url": 'https://topribejaia.com/product-category/fruits-legumes/page/1/', "category": 'Fruits et Légumes'},
        {"url": 'https://topribejaia.com/product-category/fruits-legumes/page/2/', "category": 'Fruits et Légumes'},
        {"url": 'https://topribejaia.com/product-category/fruits-legumes/page/3/', "category": 'Fruits et Légumes'},
        {"url": 'https://topribejaia.com/product-category/fruits-legumes/page/4/', "category": 'Fruits et Légumes'},
        {"url": 'https://topribejaia.com/product-category/fruits-legumes/page/4/', "category": 'Fruits et Légumes'},
        {"url": 'https://topribejaia.com/product-category/fruits-secs/page/1/', "category": 'Fruits Secs'},
        {"url": 'https://topribejaia.com/product-category/fruits-secs/page/2/', "category": 'Fruits Secs'},
        {"url": 'https://topribejaia.com/product-category/semoulerie-farine/', "category": 'Semoulerie et Farine'}       
        ]
    for item in urls:
        url = item["url"]
        category = item["category"]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        products_container = soup.find("ul", class_="products")
        products = products_container.find_all("li", class_="ast-col-sm-12")
        
        for prod in products:
            
            box = prod.find("div", class_="astra-shop-summary-wrap")
            name = box.find("a")
            href = name.get("href") if name else None
            subpage = requests.get(href)
            soup = BeautifulSoup(subpage.text, "html.parser")
            product = soup.find("div", class_="summary")
            name = product.find("h1", class_="product_title")
            if name:
                name = name.text.strip() if name else None
            price = product.find("p", class_="price")
            if price:
                price = price.text.strip() if price else None
            data.append({
                "Name": name,
                "Price": price,
                "Category": category
            })
            time.sleep(0.1)   
    df = pd.DataFrame(data)
    df.to_csv("data/products2.csv", index=False, encoding="utf-8-sig")
    print("Data 2 Saved Successfully")
if __name__ == "__main__":
    start = time.time()
    scrape()
    end = time.time()
    print(f"Execution time: {end - start:.4f} seconds")