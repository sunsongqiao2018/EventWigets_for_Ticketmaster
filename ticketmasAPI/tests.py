import json
import pandas as pd
import ijson
import asyncio

# 91649 events

pass_in_file = None


def main():
    # done
    print("started")
    # json_split()
    # alter_json_format()
    json_stream_decoder()
    # event_json_cleaning()
    # test_attraction()
    print("finished")


def alter_json_format():
    data = open('US.json')
    print("started loading")
    data = json.load(data)
    event_list = data["events"]
    print(event_list[0])

    # with open("newTest.json",'w+') as testfile:


def json_split_test():
    count = 0
    data = open('SavedEvent.json')
    print("started loading")
    data = json.load(data)

    event_list = data["events"]
    for event in event_list:
        with open(f"spilter{count}.txt", "w") as outfile:
            json.dump(event, outfile)
        print(f"working on {count} file")
        outfile.close()
        count += 1


def json_split():
    count = 0
    data = open('US.json')
    print("started loading")
    data = json.load(data)

    event_list = data["events"]
    # with open(f"newjsonfiles/spilter{count}","w+") as outfile:
    # event = event_list[0]
    # json.dump(event,outfile,separators=(',', ':'),indent=4)
    for event in event_list:
        with open(f"newjsonfiles/spilter{count}", "w+") as outfile:
            json.dump(event, outfile, separators=(',', ':'))
        print(f"working on {count} file")
        outfile.close()
        count += 1


# async def json_stream_decoder():

def json_stream_decoder():
    print("called")
    value = input("enter value ")

    if int(value) == 0:
        # use json package.
        data = open('US.json')
        print("started in json lib")
        data = json.load(data)
        print("finished in json lib")

    else:
        filenurl = "/Users/songqiaosun/Documents/JsonSpliter/US.json"
        f = open(filenurl, "r")
        print("started ijson load")
        event_objects = ijson.items(f, 'events.item')
        events_final = []
        for event in event_objects:
            cleaned_event = yield event_json_cleaning(event)
            cleaned_event_object = {"event": cleaned_event}
            events_final.append(cleaned_event_object)
            print(event)
            # await asyncio.sleep(1)
            # go_on_button = input("want to keep going?")
            # if int(go_on_button) == 1:
            #     break

        output_event = {'events': events_final}
        with open("test.json", 'w+') as infile:
            json.dump(output_event, infile, indent=4, separators=(',', ':'))
            print("writing new file")


# asyncio.run(json_stream_decoder())


def event_json_cleaning(event_data):
    # # TODO open file
    # mode = "r"
    # open_file = 'US.json'

    # data = open(open_file, 'r')
    # print("open data")
    # events = json.load(data)
    # # load json
    # events_list = events['events']
    # # events_cleaned = []
    # for filename in events_list:
    # filename = json.load(data)
    # filtering factors
    filename = event_data
    if filename is not None:
        event_id = filename["eventId"]
        legacyEventId = filename["legacyEventId"]
        primary_event_url = filename["primaryEventUrl"]

        event_name = filename["eventName"]
        event_status = filename["eventStatus"]
        event_start_time = filename["eventStartDateTime"]
        event_image_url = filename["eventImageUrl"]
        event_start_local_time = filename["eventStartLocalTime"]
        event_start_local_date = filename['eventStartLocalDate']

        venue = filename["venue"]
        # venue longti & lati for mapping
        venue_name = venue["venueName"]
        venue_id = venue["venueId"]
        venue_legacy_id = venue['legacyVenueId']
        venue_latitude = venue['venueLatitude']
        venue_longitude = venue['venueLongitude']
        venue_street = venue['venueStreet']
        venue_city = venue["venueCity"]
        venue_state_code = venue["venueStateCode"]
        venue_country_code = venue["venueCountryCode"]

        # may have multi attractions
        attractions = filename["attractions"]

        min_price = filename["minPrice"]
        max_price = filename["maxPrice"]
        currency = filename["currency"]
        on_sale_start_date = filename["onsaleStartDateTime"]
        on_sale_end_date = filename["onsaleEndDateTime"]
        source = filename["source"]
        hot_event = filename["hotEvent"]

        # extract attractions
        attraction_extr = []
        for attr in attractions:
            attr_detail = attr["attraction"]
            attr_id = attr_detail["attractionId"]
            attr_name = attr_detail['attractionName']
            attr_img_list = attr_detail['images']
            attr_img = []
            if attr_img_list.__len__() > 0:
                attr_img = attr_img_list[0]['image']['url']
            classfication_segment = attr_detail['classificationSegment']
            classfication_genre = attr_detail['classificationGenre']
            classfication_sub_genre = attr_detail['classificationSubGenre']
            classfication_type = attr_detail['classificationType']
            resemble_attr = {"attraction_id": attr_id, "attraction_name": attr_name, 'attraction_img_url': attr_img,
                             'segment': classfication_segment, 'genre': classfication_genre,
                             'sub_genre': classfication_sub_genre, 'type': classfication_type}
            attraction_extr.append(resemble_attr)
        # gather factors
        event_json = {"event_id": event_id, "primary_event_url": primary_event_url, "event_name": event_name,
                      "event_status": event_status, 'event_image_url': event_image_url,
                      "event_start_time": event_start_local_time,
                      "event_local_time": {'event_start_local_time': event_start_local_time,
                                           'event_start_local_date': event_start_local_date},
                      'venue': {'venue_name': venue_name, 'venue_id': venue_id,
                                'venue_address': {'venue_street': venue_street, 'venue_city': venue_city,
                                                  'venue_state_code': venue_state_code,
                                                  'venue_country_code': venue_country_code},
                                "venue_latitude": venue_latitude, 'venue_longitude': venue_longitude},
                      "attractions": attraction_extr,
                      'min_price': min_price, 'max_price': max_price, 'currency': currency,
                      'on_sale_start_date': on_sale_start_date, 'on_sale_end_date': on_sale_end_date,
                      'source': source, 'hot_event': hot_event}
        # TODO return a json file to upper function

        event_cleaned = {"event": event_json}
    return event_cleaned
    #     events_cleaned.append(event_cleaned)

    # # write to new json file

    # output_event = {'events': events_cleaned}
    # with open("test.json", 'w+') as infile:
    # 	json.dump(output_event, infile, indent=4, separators=(',', ':'))
    # 	print("writing new file")


def test_attraction():
    data = open("spilter0", 'r')
    data = json.load(data)
    attractions = data['attractions']
    for attraction in attractions:
        attr_url = attraction['attraction']['images'].__len__()
        print(attr_url)


main()