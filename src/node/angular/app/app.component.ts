import { Component } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  public title: string = '{{ should say "pong" }}';

  constructor() {
    const socketUrl: string = `ws://${
      window.location.toString().split('//')[1]
    }api/ping`;
    console.log('socketUrl', socketUrl);
    const socket$: WebSocketSubject<any> = webSocket(socketUrl);

    socket$.subscribe(
      (msg: string) => {
        this.title = msg;
      },
      (err: Error) => console.log(err),
      () => console.log('complete'),
    );

    socket$.next(JSON.stringify({ op: 'hello' }));
  }
}
