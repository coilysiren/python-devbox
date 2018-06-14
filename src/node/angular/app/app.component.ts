import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  public title: string = '{{ should say "pong" }}';

  constructor(http: HttpClient) {
    http.get('/api/ping').subscribe((responseData: any) => {
      this.title = responseData.data;
    });
  }
}
