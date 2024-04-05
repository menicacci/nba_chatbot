import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { ChatComponent } from './chat/chat.component';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import { MessageComponent } from './chat/message/message.component';


@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    MessageComponent
  ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpClientModule,
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
