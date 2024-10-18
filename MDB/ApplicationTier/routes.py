from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from model import RNG
from db_var import collection_name

router = APIRouter()


# These are all definitions for 'get' requests. The functions that they are responsible for are found in the response_discription argument.
@router.get("/", response_description="List all pulses", response_model=List[RNG])
def list_pulses(request: Request):
    pulse = list(request.app.database[collection_name].find())  # The limit here was 100. This was causing the maximum index not exceeding 100. There are two ways to solve this problem. A: set the limit to be 0. B: delete the "limit" parameter, which makes it ~.find(). This "~.find()" according to MongoDB returns all the documents in a collection. In my understanding it is the same as "~.find({})", where there is nothing in the query bracket, and no projection bracket has been specified.
    return pulse


@router.get("/last", response_description="Return the last pulse", response_model=List[RNG])
def last_pulse(request: Request):
    pulse = list(request.app.database[collection_name].find().sort({'_id': -1}).limit(1))
    return pulse
    # if (pulse := list(request.app.database[collection_name].find().sort('_id', -1).limit(1))[0]) is not None:
    #     return pulse
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"last pulse not found")


@router.get("/chainIndexandpulseIndex", response_description="Get a single pulses by chainindex and pulseindex", response_model=RNG)
def find_pulse(chainIndex: str, pulseIndex: str, request: Request):
    if (pulse := request.app.database[collection_name].find_one({"chainIndex": int(chainIndex), "pulseIndex": int(pulseIndex)})) is not None:
        return pulse
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"pulse with chainIndex {int(chainIndex)} and pulseIndex {int(pulseIndex)} not found")


@router.get("/chainIndexandpulseIndex_year", response_description="Locate the year pulse by the current chainindex and pulseindex", response_model=RNG)
def find_pulse(chainIndex: str, pulseIndex: str, request: Request):
    if (pulse := request.app.database[collection_name].find_one({"chainIndex": int(chainIndex), "pulseIndex": (int(pulseIndex))})) is not None:
        year_outputValue = pulse["listValues"][4]["value"]
        if year_outputValue != "THIS_IS_THE_FIRST_PULSE_OR_YEAR_DID_NOT_FOUND":
            year_pulse = request.app.database[collection_name].find_one({"outputValue": year_outputValue})
            return year_pulse
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="THIS_IS_THE_FIRST_PULSE_OR_YEAR_WAS_NOT_FOUND")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"pulse with chainIndex {int(chainIndex)} and pulseIndex {int(pulseIndex)} not found")


@router.get("/chainIndexandpulseIndex_month", response_description="Locate the month pulse by the current chainindex and pulseindex", response_model=RNG)
def find_pulse(chainIndex: str, pulseIndex: str, request: Request):
    if (pulse := request.app.database[collection_name].find_one({"chainIndex": int(chainIndex), "pulseIndex": (int(pulseIndex))})) is not None:
        month_outputValue = pulse["listValues"][3]["value"]
        if month_outputValue != "THIS_IS_THE_FIRST_PULSE_OR_MONTH_DID_NOT_FOUND":
            month_pulse = request.app.database[collection_name].find_one({"outputValue": month_outputValue})
            return month_pulse
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="THIS_IS_THE_FIRST_PULSE_OR_MONTH_WAS_NOT_FOUND")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"pulse with chainIndex {int(chainIndex)} and pulseIndex {int(pulseIndex)} not found")


@router.get("/chainIndexandpulseIndex_day", response_description="Locate the day pulse by the current chainindex and pulseindex", response_model=RNG)
def find_pulse(chainIndex: str, pulseIndex: str, request: Request):
    if (pulse := request.app.database[collection_name].find_one({"chainIndex": int(chainIndex), "pulseIndex": (int(pulseIndex))})) is not None:
        day_outputValue = pulse["listValues"][2]["value"]
        if day_outputValue != "THIS_IS_THE_FIRST_PULSE_OR_DAY_DID_NOT_FOUND":
            day_pulse = request.app.database[collection_name].find_one({"outputValue": day_outputValue})
            return day_pulse
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="THIS_IS_THE_FIRST_PULSE_OR_DAY_WAS_NOT_FOUND")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"pulse with chainIndex {int(chainIndex)} and pulseIndex {int(pulseIndex)} not found")


@router.get("/chainIndexandpulseIndex_hour", response_description="Locate the hour pulse by the current chainindex and pulseindex", response_model=RNG)
def find_pulse(chainIndex: str, pulseIndex: str, request: Request):
    if (pulse := request.app.database[collection_name].find_one({"chainIndex": int(chainIndex), "pulseIndex": (int(pulseIndex))})) is not None:
        hour_outputValue = pulse["listValues"][1]["value"]
        if hour_outputValue != "THIS_IS_THE_FIRST_PULSE_OR_HOUR_DID_NOT_FOUND":
            hour_pulse = request.app.database[collection_name].find_one({"outputValue": hour_outputValue})
            return hour_pulse
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="THIS_IS_THE_FIRST_PULSE_OR_HOUR_WAS_NOT_FOUND")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"pulse with chainIndex {int(chainIndex)} and pulseIndex {int(pulseIndex)} not found")


@router.get("/chainIndexandpulseIndex_previous", response_description="Locate the previous pulse by the current chainindex and pulseindex", response_model=RNG)
def find_pulse(chainIndex: str, pulseIndex: str, request: Request):
    if (pulse := request.app.database[collection_name].find_one({"chainIndex": int(chainIndex), "pulseIndex": (int(pulseIndex))})) is not None:
        prev_outputValue = pulse["listValues"][0]["value"]
        if prev_outputValue != "THIS_IS_THE_FIRST_PULSE_OR_HOUR_DID_NOT_FOUND":
            prev_pulse = request.app.database[collection_name].find_one({"outputValue": prev_outputValue})
            return prev_pulse
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="THIS_IS_THE_FIRST_PULSE_OR_THE_PREVIOUS_LINKED_PULSE_WAS_NOT_FOUND")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"pulse with chainIndex {int(chainIndex)} and pulseIndex {int(pulseIndex)} not found")


# At the end I added an example about post method for reference too.
# @router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
# def create_book(request: Request, book: Book = Body(...)):
#     book = jsonable_encoder(book)
#     new_book = request.app.database["books"].insert_one(book)
#     created_book = request.app.database["books"].find_one(
#         {"_id": new_book.inserted_id}
#     )
