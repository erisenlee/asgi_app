import responder,graphene
import time


api = responder.API(debug=True)

@api.route('/')
async def index(req, resp):
    resp.media = {"hello":req.url}


@api.route("/incoming")
async def receive_incoming(req, resp):

    @api.background.task
    def process_data(data):
        """Just sleeps for three seconds, as a demo."""
        time.sleep(3)

    # Parse the incoming data as form-encoded.
    # Note: 'json' and 'yaml' formats are also automatically supported.
    data = await req.media()

    # Process the data (in the background).
    process_data(data)

    # Immediately respond that upload was successful.
    resp.media = {'success': True}

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    gender = graphene.String(name=graphene.String(default_value="MA"))

    def resolve_hello(self, info, name):
        return f"Hello {name}"
    def resolve_genger(self, info, name):
        return f"gends {name}"

schema = graphene.Schema(query=Query)
view = responder.ext.GraphQLView(api=api, schema=schema)

api.add_route("/graph", view)


if __name__ == "__main__":
    api.run(debug=True)