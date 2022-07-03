from ninja import Router, Schema, errors
import os


posts_controller = Router()
data = {}
path = "posts/"
extension = ".md"


class DataSchema(Schema):
    title: str
    content: str


class ContentSchema(Schema):
    content: str


@posts_controller.get('')
def list_posts(request):
    files = os.listdir("posts/")

    for i in range(len(files)):
        with open(path + files[i]) as content:
            lines = content.readlines()
            data[os.path.splitext(files[i])[0]] = lines
    return data


@posts_controller.get('{title}')
def list_post(request, title: str):
    files = os.listdir("posts/")
    if (title + extension) in files:
        with open(path + title + extension) as post:
            content = post.readlines()
            return {title: content}


@posts_controller.post('')
def post_posts(request, data_in: DataSchema):

    files = os.listdir("posts/")

    if not (data_in.title + extension) in files:

        with open(path + data_in.title + extension, 'w') as file:
            file.write(data_in.content)

        files = os.listdir("posts/")

        for i in range(len(files)):
            with open(path + files[i]) as content:
                lines = content.readlines()
                data[os.path.splitext(files[i])[0]] = lines

        return data

    else:
        return {"status": "Not created, file already exist", "files": os.listdir("posts/")}


@posts_controller.put('{title}')
def post_update(request, title: str, content: ContentSchema):

    files = os.listdir("posts/")

    if (title + extension) in files:
        with open(path + title + extension, 'w') as file:
            file.write(content.content)
        with open(path + title + extension) as new_file:
            return {"status": "Successfully updated", "new_data": {title: new_file.readlines()}}

    else:
        return "There is no such file"


@posts_controller.delete('{title}')
def post_delete(request, title: str):

    files = os.listdir("posts/")

    if (title + extension) in files:
        os.remove(path + title + extension)
        return {"status": "Successfully deleted", "new_data": os.listdir("posts/")}

    else:
        return {"status": "Not deleted, there is no such file", "new_data": os.listdir("posts/")}
