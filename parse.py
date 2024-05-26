import random
def parse(soup):
  gameid = []
  title = []
  pricenodiscount = []
  pricediscount = []
  rating = []
  reviews = []
  isdiscount = []
  platforms = []
  allplatforms = []

  for game in soup.find_all('a', {"class": "search_result_row ds_collapse_flag"}):
    try:
      gameid.append(game['data-ds-appid'])
    except:
      randid = random.randint(10000000, 50000000)
      while randid in gameid:
        randid = random.randint(10000000, 50000000)
      gameid.append(randid)
    title.append(game.find('span', {"class": "title"}).text)
    # try:
    #   print(game.findAll('div', {"class": "discount_final_price"})[0].findAll("div")[1].text.split()[0])
    # except:
    #   print("-")
    try:
      pnd = game.find('div', {"class": "discount_original_price"}).text.split()[0]
      pd = game.find('div', {"class": "discount_final_price"}).text.split()[0]
    except:
      try:
        pnd = game.find('div', {"class": "discount_final_price"}).text.split()[0]
        pd = game.find('div', {"class": "discount_final_price"}).text.split()[0]
        if pnd == "Бесплатно":
          pnd = 0
          pd = 0
      except:
          pnd = 0
          pd = 0
    try:

    
      pd = game.findAll('div', {"class": "discount_final_price"})[0].findAll("div")[1].text.split()[0]
    except:
      pass
    pricenodiscount.append(pnd)
    pricediscount.append(pd)
    #Записываю процент оценки
    try:
      rating.append(game.find("span", {"class": "search_review_summary"})["data-tooltip-html"].split("%")[0][-2:])
      reviews.append(game.find("span", {"class": "search_review_summary"})["data-tooltip-html"].split("%")[1].split()[1].replace(",", ""))
    except:
      rating.append("0")
      reviews.append("0")
    discounttemp = False
    if pnd != pd:
      discounttemp = True
    isdiscount.append(discounttemp)
    

    tempplatforms = []
    for platform in game.find('div', {"class": "col search_name ellipsis"}).div.findAll("span"):
      try:
        if platform.attrs['class'][1] != "group_separator":
          tempplatforms.append(platform.attrs['class'][1])
          if not platform.attrs['class'][1] in allplatforms:
            allplatforms.append(platform.attrs['class'][1])
      except:
        if not 'includes' in platform.attrs['class'][0]:
          tempplatforms.append(platform.attrs['class'][0])
          if not platform.attrs['class'][0] in allplatforms:
            allplatforms.append(platform.attrs['class'][0])
      platforms.append(tempplatforms)
    print(game.find('span', {"class": "title"}).text, pd)
  return {"gameid": gameid, "title": title, "pricenodiscount": pricenodiscount, "pricediscount": pricediscount, "rating": rating, "reviews": reviews, "isdiscount": isdiscount, "platforms": platforms, "allplatforms": allplatforms}

  