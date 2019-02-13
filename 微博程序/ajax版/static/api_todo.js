class TodoApi {
    static basePath = '/api/todo'

    constructor() {
    }

    static all(callback) {
        const path = `${this.basePath}/all`
        fetch(path)
            .then(res => res.json())
            .then(data => {
                callback(data)
            })
    }

    static add(form, callback) {
        const path = `${this.basePath}/add`
        const options = {
            method: 'POST',
            body: JSON.stringify(form),
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
        }
        fetch(path, options)
            .then(res => res.json())
            .catch(error => console.log('error', error))
            .then(data => {
                callback(data)
            })
    }

    static delete(id, callback) {
        const path = `${this.basePath}/delete?id=${id}`
        fetch(path)
            .then(res => res.json())
            .then(data => {
                callback(data)
            })
    }

    static update(form, callback) {
        const path = `${this.basePath}/update`
        const options = {
            method: 'POST',
            body: JSON.stringify(form),
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
        }

        fetch(path, options)
            .then(res => res.json())
            .catch(error => console.log(error))
            .then(data => {
                callback(data)
            })
    }

}