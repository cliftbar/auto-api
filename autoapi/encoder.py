import flask


class AutoAPIObjEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if 'to_dict' in dir(obj):
            return obj.to_dict()

        return super(obj)
