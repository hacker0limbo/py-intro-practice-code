const todoTemplate = (todo) => {
    const title = todo.title
    const id = todo.id
    const t = `
        <div class="todo-cell" id='todo-${id}' data-id="${id}">
            <span class='todo-title'>${title}</span>
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">删除</button>
        </div>
        `
    return t
}

const insertEditForm = (cell) => {
    const form = `
        <div class='todo-edit-form'>
            <input class="todo-edit-input">
            <button class='todo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}


class Todo {
    constructor() {
        this.todoListDiv = e('.todo-list')
        this.init()
    }

    init() {
        this.loadTodos()
        this.bindEvents()
    }

    insertTodo(todo) {
        // 用来插入一条 todo 数据
        const todoCell = todoTemplate(todo)
        appendHtml(this.todoListDiv, todoCell)
    }

    bindEvents() {
        this.bindEventAdd()
        this.bindEventDelete()
        this.bindEventEdit()
        this.bindEventUpdate()
    }

    loadTodos() {
        TodoApi.all(todos => {
            for (let i = 0; i < todos.length; i++) {
                const todo = todos[i]
                this.insertTodo(todo)
            }
        })
    }

    bindEventAdd() {
        const addBtn = e('#id-button-add')
        bindEvent(addBtn, 'click', event => {
            const input = e('#id-input-todo')
            const title = input.value
            const form = {
                title: title,
            }
            TodoApi.add(form, todo => {
                this.insertTodo(todo)
            })
        })
    }

    bindEventDelete() {
        // 事件委托
        bindEvent(this.todoListDiv, 'click', event => {
            const target = event.target
            if (target.classList.contains('todo-delete')) {
                const todoCell = target.parentElement
                const todo_id = todoCell.dataset.id
                TodoApi.delete(todo_id, data => {
                    console.log('删除的数据为: ', data)
                    todoCell.remove()
                })
            }
        })
    }

    bindEventEdit() {
        bindEvent(this.todoListDiv, 'click', event => {
            const target = event.target
            if (target.classList.contains('todo-edit')) {
                const todoCell = target.parentElement
                insertEditForm(todoCell)
            }
        })
    }

    bindEventUpdate() {
        bindEvent(this.todoListDiv, 'click', event => {
            const target = event.target
            if (target.classList.contains('todo-update')) {
                const editForm = target.parentElement
                const title = editForm.querySelector('.todo-edit-input').value
                const todoCell = target.closest('.todo-cell')
                const todo_id = todoCell.dataset.id
                const form = {
                    id: todo_id,
                    title: title,
                }
                TodoApi.update(form, todo => {
                    const titleSpan = todoCell.querySelector('.todo-title')
                    titleSpan.innerHTML = todo.title
                })
            }
        })
    }
}


const __main = () => {
    todoController = new Todo()
}

__main()