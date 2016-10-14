# -*- coding: utf-8 -*-
import requests
import bs4
#comment
stores=["Asda","Tesco","Sainsburys","Morrisons","Waitrose","Ocado","Aldi","M_and_S","Iceland","Amazon","Boots","Poundland","Poundstretcher"]

def get_all_prices(product="heineken",multiplier=1):
    results=[]
    total=0
    for store in stores:
        get_prices(store,product,results,multiplier)
    results=sorted(results,key=lambda x:x[2])
    if results:
        tooltip=""
        for item in results:
            total += item[2]
        av=total / len(results)
        average = convert_price(round(av,2))
        below_price=str(round(round((av-results[0][2])/av,2)*100,0))+"%"
        discount="Av: "+average+" -"+str(below_price)+ " "
        if len(results)>1:
            tooltip=str(results[1][0])+" "+convert_price(results[1][2])
        if len(results)>2:
            tooltip+= " " + str(results[2][0]) + " " + convert_price(results[2][2])
        results[0]+=[tooltip]
        results[0]+=[" ("+discount+")"]
        print (tooltip,discount)

    return results

def get_prices(store="Tesco",product="Heineken",results=[],multiplier=1):

    link=""
    promotion=""
    web_url="http://www.mysupermarket.co.uk/Shopping/FindProducts.aspx?query="+product+"&store="+store
    print (web_url)
    res = requests.get(web_url)
    html=bs4.BeautifulSoup(res.text, "html.parser")
    items=html.find_all("div",{"class":"DetailsWrp"})
    for item in items:
        ci=item.find_all("h3",{"class":"Name"})
        product_name = ci[0].text.replace("\n", "")
        pi=item.find_all("div",{"class":"PpuWrp"})
        for p in pi:
            if p.find_all("span", {"class": "AfterOffer"}):
                price = p.find_all("span", {"class": "AfterOffer"})[0].text.replace("/", "")
                price_per=p.find_all("span")[0].text
                if price_per.count("/") == 2:
                    end=len(price_per)
                    start=price_per.index("/")
                    if (start +2) < end and start != -1:
                        price_per=price_per[start+2:end]
                break
            elif p.find_all("span", {"class": "BeforeOffer"}):
                price = p.find_all("span", {"class": "BeforeOffer"})[0].text.replace("/", "")
                price_per = p.find_all("span")[0].text
        if "p" in price:
            price = price.replace("p", "")
            price = round(float(price) * multiplier / 100, 2)
        else: #remove any non ascii chars such as £ sign
            price = ''.join(a for a in price if ord(a) < 128)
            price = round(float(price) * multiplier, 2)
            #elif "£" in price:
         #   price = price.replace("£", "")
            #price = round(float(price) * multiplier, 2)
        ap = item.find_all("span", {"class": "Price"})
        apoff = item.find_all("span", {"class": "Offer"})
        if apoff:
            actual_price = apoff[0].text.replace("\n", "")
        else:
            actual_price =ap[0].text.replace("\n", "")
        # 4. Promotion if any
        prom = item.find_all("a", {"id": "Offer"})
        if prom:
            promotion =  prom[0].text.replace("\n", "")

        link=get_product_link(store,product,product_name)

        remove_list=["Alcoholic","Alcohol","4%","Cidre","Free","Tonic","Lime","Orange","WKD","Cranberry","Garlic","Sweet","BBQ","Verde","Cola"]
        #if "4%" not in product_name and "Cidre" not in product_name and "Free" not in product_name :
        if not any(word in product_name for word in remove_list):
            results+=[[store,product_name,price,link,actual_price,promotion,price_per]]

def get_product_link(store,product,product_name):
    # cos ive now added price into product_name will have to search by just product for now
    link=""
    if store == "Tesco":
        link = "http://www.tesco.com/groceries/product/search/default.aspx?searchBox=" + product #product_name accepted
    elif store == "Aldi":
        link = "https://www.aldi.co.uk/search?text=" + product
    elif store == "Morrisons":
        link = "https://groceries.morrisons.com/webshop/getSearchProducts.do?clearTabs=yes&isFreshSearch=true&chosenSuggestionPosition=&entry=" + product
    elif store == "Asda":
        link = "https://groceries.asda.com/search/" + product #product_name accepted
    elif store == "Sainsburys":
        link = "https://www.sainsburys.co.uk/shop/gb/groceries/" + product #product_name accepted
    elif store == "Ocado":
        link = "https://www.ocado.com/webshop/getSearchProducts.do?clearTabs=yes&isFreshSearch=true&chosenSuggestionPosition=&entry=" + product
    elif store == "Waitrose":
        link = "http://www.waitrose.com/shop/HeaderSearchCmd?searchTerm=" + product
    elif store == "Iceland":
        link = "http://groceries.iceland.co.uk/search?text=" + product
    return link

def convert_price(price):
    price="£"+str(price)
    pos=price.index(".")
    if len(price)-price.index(".")==2:
        price+="0"
    return price