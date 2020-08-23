## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy


## say goodbye
* goodbye
  - utter_goodbye


## fire update
* fire_update
    - action_fire_update
    - form{"name": "action_fire_update"}
    - form{"name": null}
  
## fire update
* greet
  - utter_greet
* fire_update
    - action_fire_update
    - form{"name": "action_fire_update"}
    - form{"name": null}


## help
* help
  - utter_help

## reset
* reset
  - utter_reset