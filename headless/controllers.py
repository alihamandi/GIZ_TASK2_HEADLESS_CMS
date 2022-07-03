from ninja import Router, Schema, errors
import os


posts_controller = Router()
data = {}
path = "posts/"
extension = ".md"


class DataSchema(Schema):
    title: str
    content: str


@posts_controller.get('')
def list_posts(request):
    files = os.listdir("posts/")

    for i in range(len(files)):
        with open(path + files[i]) as content:
            lines = content.readlines()
            data[os.path.splitext(files[i])[0]] = lines
    return data


@posts_controller.post('')
def post_posts(request, data_in: DataSchema):

    with open(path + data_in.title + extension, 'w') as file:
        file.write(data_in.content)

    return os.listdir("posts/")


@posts_controller.put('')
def post_update(request, post: DataSchema):

    files = os.listdir("posts/")
    print(files)
    if (post.title + extension) in files:
        with open(path + post.title + extension, 'w') as file:
            file.write(post.content)
        with open(path + post.title + extension) as new_file:
            return {"status": "Successfully updated", "new_data": {post.title: new_file.readlines()[0]}}
    else:
        return "There is no such file"


@posts_controller.delete('{in_file_name}')
def post_delete(request, in_file_name: str):
    file_name = in_file_name.split(".")[0]
    files = os.listdir("posts/")

    if (file_name + extension) in files:
        os.remove(path + file_name + extension)
        return {"status": "Successfully deleted", "new_data": os.listdir("posts/")}

    else:
        return "There is no such file"
