import { Component } from '@angular/core';
import {ApiService} from "../api.service";
import {SenderRoles} from "../data/constants";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {

  messages: {sender: string, content: string}[] =
    [
      { sender: SenderRoles.BOT,  content: 'Hello! How can I assist you today?' }
    ];

  newMessage: string = '';
  inputActive: boolean = true;

  chatName = "Chatbot"

  constructor(private apiService: ApiService) {}

  sendMessage() {
    this.messages.push({ sender: SenderRoles.USER, content: this.newMessage });

    this.inputActive = false;
    this.apiService.sendRequest(this.newMessage)
      .subscribe((response: any) => {
        this.inputActive = true;
        this.messages.push({sender: SenderRoles.BOT, content: response.response})
      });

    this.newMessage = '';
  }

  isSenderUser(sender: string) {
    return sender === SenderRoles.USER;
  }
}
