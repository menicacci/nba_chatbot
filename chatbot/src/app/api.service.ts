import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  sendRequest(inputString: string): Observable<any> {
    return this.http.post<any>(environment.serverBasePath, { message: inputString });
  }

}
