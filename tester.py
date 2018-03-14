

post_details = {
    "details": {
        "child_count": 1,
        "children": "baboo"
    },
    "hasPrev": False
}

if __name__ == '__main__':
    post_details['info'] = {"lat":0.0,"long":1.0}
    print(post_details)

    # Should then be
    result = {'hasPrev': False,
              'info': {'lat': 0.0, 'long': 1.0},
              'details': {'child_count': 1, 'children': 'baboo'}
              }
