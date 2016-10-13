# django-tastypie-specific-fields
### A tastypie extension that allows you to specify the fields you are interested in.

Django tastypie specific fields is a light and simple, but very usefull extension for django-tastypie. It allows you to get from a resource only the fields and/or related resources you are interested in. It is so flexible that you can make very specific requests lookup by specifying the fields you want at a very deep level in relatedness hierarchy starting from the main resource.

For example let us consider the publisher model (*found in the example given with the project*) which has *id, prefix, title and website* as fields. The response for the following request _GET http://path/to/my/app/api/v1/publisher/?**fields=title,website**&format=json_ will be

    {
        meta: {
            ...
        },
        objects: [
            {
                title: "Publisher1",
                website: "http://www.publisher1.com"
            },
            {
                title: "Publisher2",
                website: "http://www.publisher2.com"
            },
            ...
        ]
    }
    
while the one for the "normal" request _GET http://path/to/my/app/api/v1/publisher/?format=json_ will be

    {
        meta: {
            ...
        },
        objects: [
            {
                id: 1,
                prefix: "pub1",
                title: "Publisher1",
                website: "http://www.publisher1.com"
            },
            {
                id: 2,
                prefix: "pub2",
                title: "Publisher2",
                website: "http://www.publisher2.com"
            },
            ...
        ]
    }
    
---------------------    
### Django-tastypie-specific-fields also supports **relative fields filtering**.

Let us consider the case where you have an author model with *profession and birthdate* as direct fields. This author is also related to a django user.
If you just want to have for an author his *profession*, the *first_name*, the *last_name* and the *id* of the related django user, you can do the following very precise request _GET http://path/to/my/app/api/v1/author/?**fields=profession,user(id,first_name,last_name)**&format=json_ which will give you the following response

    {
        meta: {
            ...
        },
        objects: [
            {
                profession: "profession2",
                user: {
                    first_name: "user2",
                    id: 3,
                    last_name: "user2"
                }
            },
            {
                profession: "profession3",
                user: {
                    first_name: "user3",
                    id: 4,
                    last_name: "user3"
                }
            },
            ...
        ]
    }
    
If you don't specify in parentheses any field of the related resource, it will give you back the whole related resource.
 _GET http://path/to/my/app/api/v1/author/?**fields=profession,user**&format=json_
 
    {
        meta: {
        ...
        },
        objects: [
            {
                profession: "profession2",
                user: {
                    date_joined: "2016-09-27T13:11:05.165000",
                    email: "user2@mysite.com",
                    first_name: "user2",
                    id: 3,
                    last_login: "2016-09-27T13:11:05.165000",
                    last_name: "user2",
                    username: "user2"
                }
            },
            {
                profession: "profession3",
                user: {
                    date_joined: "2016-09-27T13:11:05.438000",
                    email: "user3@mysite.com",
                    first_name: "user3",
                    id: 4,
                    last_login: "2016-09-27T13:11:05.438000",
                    last_name: "user3",
                    username: "user3"
                }
            },
            ...
        ]
    }
    
### Django-tastypie-specific-fields also have a very good support of **m2m(ManyToMany) relations**
If you specify some fields to retreive from a m2m related resources, you will be given back the set of those related resources. But each element of this set will contain only the fields you need.
In our example, a book can have many *authors* and also many *genres*.
Here is the response for the _GET http://path/to/my/app/api/v1/book/?**fields=title,genres(title),authors(profession,user)**&format=json_ request.

    {
        meta: {
            ...
        },
        objects: [
            {
            authors: [
                {
                    profession: "profession3",
                    user: {
                        date_joined: "2016-09-27T13:11:05.438000",
                        email: "user3@mysite.com",
                        first_name: "user3",
                        id: 4,
                        last_login: "2016-09-27T13:11:05.438000",
                        last_name: "user3",
                        username: "user3"
                    }
                },
                {
                    profession: "profession2",
                    user: {
                        date_joined: "2016-09-27T13:11:05.650000",
                        email: "user4@mysite.com",
                        first_name: "user4",
                        id: 5,
                        last_login: "2016-09-27T13:11:05.650000",
                        last_name: "user4",
                        username: "user4"
                    }
                }
            ],
            genres: [
                {
                    title: "genre1"
                },
                {
                    title: "genre2"
                },
                {
                    title: "genre3"
                }
                ],
                    title: "Book 1"
                },
            ]
            ...
        ]
    }

### Advanced related resource fields lookup
Django-tastypie-specific-fields implements a recursive lookup process to get the specific fields you need.
For this reason, you can specify the fields you want from a resource that is related to a related one, and so on.
This simply means that you are allowed to do requests like the following: 
    
    path/to/my/app/api/v1/resource/?fields=field1,resource1(field11,resource12(resource21(field31,field32))

*However, this will not work with ManyToMany relations*

### Acknowledgements
Thanks to:
* Florentin Jiechieu
* Hubert Noyessie
* Franklin Mbouopda
