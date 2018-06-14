import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

interface ITodo {
  content: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  public todos: ITodo[];

  constructor(private http: HttpClient) {
    this.updateTodos();
  }

  public async createTodo(event: Event, content: string): Promise<void> {
    event.preventDefault();
    if (content) {
      this.http.post('/api/todos', { data: content }).subscribe(() => {
        // update todo list after you add this todo
        this.updateTodos();
      });
    }
  }

  public async deleteTodo(id: string): Promise<void> {
    await this.http.delete(`/api/todos/${id}`).subscribe(() => {
      // update todo list after you delete this todo
      this.updateTodos();
    });
  }

  public updateTodos(): void {
    this.http.get('/api/todos').subscribe((response: any) => {
      this.todos = response;
    });
  }
}
