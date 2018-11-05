import connexion

def api():

    app = connexion.App("service", specification_dir='/opt/pi-k8s/openapi')
    app.add_api('service.yaml')

    return app

ITEMS = [
    {
        "id": 1,
        "name": "people"
    },
    {
        "id": 2,
        "name": "stuff"
    },
    {
        "id": 3,
        "name": "things"
    }
]

def item_list():

    return ITEMS

def item_retrieve(item_id):

    for item in ITEMS:
        if item["id"] == item_id:
            return item

    return {"message": "Not Found"}, 404

