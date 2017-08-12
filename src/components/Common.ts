import { AddressInterface } from "./Common"

export interface StrIndex<TValue> {
  [key: string]: TValue
}
export interface AddressInterface {
  post_area: string;
  post_code: number;
  street_name?: string;
}

export interface AddressFullInterface extends AddressInterface {
  address1: string;
  address2: string;
}

export const enum HTTPVerbs {
  post = 'POST',
  get = 'GET',
  put = 'PUT',
  delete = 'DELETE',
  patch = 'PATCH'
}

export class ByID {
  list: KnockoutObservableArray<any>
  constructor(list: any[]) {
    this.list = ko.observableArray(list)
  }
  by_id(id: number) {
    for (let item of this.list()) {
      if (item.id() == id) {
        return item
      }
    }
  }
}
export abstract class Post {
  abstract id: KnockoutObservable<number>;
  abstract serialize(): {}
  abstract save(): void
  abstract set(result: any): void
  abstract url: string
  post = (h: any, event: Event, data_object?: any, url?: string) => {
    // Abstract class for posting data. Will use PUT if id > 0
    // Also handles buttons
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let data = data_object || this.serialize()
    if (this.id() >= 0) {
      method = HTTPVerbs.put
    } else {
      method = HTTPVerbs.post
    }
    $.ajax({
      url: url || this.url,
      type: method,
      contentType: "application/json; charset=utf-8",
      dataType: 'json',
      data: JSON.stringify(data),
    }).done((result: any) => {
      this.save()
      if (method == HTTPVerbs.post) {
        this.set(result)
      } else if (method == HTTPVerbs.put) {
      }
      setTimeout(() => {
        btn.text('Endre')
      }, 20)
    }).always(function(data) {
      btn.button('reset')
    })
  }
  constructor() { }
}
