import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit {

  constructor() { }

  @Input() isUser: boolean = true;
  @Input() text: string = '';

  ngOnInit(): void {
  }

}
