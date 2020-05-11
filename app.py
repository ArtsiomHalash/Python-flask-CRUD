from flask import Flask, render_template, redirect, request
import json
import math

app = Flask(__name__)

users = [{"id": "1", "email": "george.bluth@reqres.in", "fname": "George", "lname": "Bluth", "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/calebogden/128.jpg"},
         {"id": "2", "email": "janet.weaver@reqres.in", "fname": "Janet", "lname": "Weaver",
             "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg"},
         {"id": "3", "email": "emma.wong@reqres.in", "fname": "Emma", "lname": "Wong",
             "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/olegpogodaev/128.jpg"},
         {"id": "4", "email": "eve.holt@reqres.in", "fname": "Eve", "lname": "Holt",
             "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/marcoramires/128.jpg"},
         {"id": "5", "email": "charles.morris@reqres.in", "fname": "Charles", "lname": "Morris",
             "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/stephenmoon/128.jpg"},
         {"id": "6", "email": "tracey.ramos@reqres.in", "fname": "Tracey", "lname": "Ramos",
             "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/bigmancho/128.jpg"}
         ]
state = {
    'users': users,
    'page': 1,
    'rows': 3
}


def pagination(users, page, rows):
    start = (page-1)*rows
    end = start+rows
    trimmedData = users[start: end]
    pages = math.ceil(len(users)/rows)
    return {
        'users': trimmedData,
        'pages': pages,
        'page': page
    }


@app.route("/", methods=['GET'])
def getAllUsersDefault():
    state['page'] = 1
    data = pagination(state['users'], state['page'], state['rows'])

    try:
        return render_template('users.html', data=data)
    except:
        return ("Some error occurred while trying to fetch data")


@app.route("/<int:page>", methods=['GET'])
def getAllUsers(page):
    state['page'] = page

    data = pagination(state['users'], state['page'], state['rows'])

    try:
        return render_template('users.html', data=data)
    except:
        return ("Some error occurred while trying to fetch data")


@app.route("/users/<string:id>", methods=['GET', 'POST'])
def getSingleUser(id):
    try:
        for x in state['users']:
            if x['id'] == id:
                user = x
        return render_template('user.html', user=user)

    except:
        return ("Some error occurred while trying to fetch data")


@app.route("/delete/<string:id>", methods=['DELETE'])
def deleteUser(id):
    try:
        print(id)
        state['users'] = [x for x in state['users'] if x['id'] != id]
        print(state['users'])
        return '', 200
    except:
        return ("Some error occurred while trying to delete user")


@app.route("/update/<string:id>", methods=['PUT'])
def updateUser(id):
    try:
        state['users'] = [request.get_json()['user'] if user['id'] ==
                          id else user for user in state['users']]
        return '', 200
    except:
        return ("Some error occurred while trying to update user")


@app.route("/create", methods=['GET', 'POST'])
def createUser():
    if request.method == 'GET':
        return render_template('createUser.html')
    else:
        try:
            user = request.get_json()['user']
            state['users'].insert(0, user)
            return '', 200
        except:
            return ("Some error occurred while trying to create user")


if __name__ == "__main__":
    app.run(debug=True)
