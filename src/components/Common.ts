import { AddressInterface } from "./Common"
var diff = require('recursive-diff');

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
    return this.list().find(myObj => {
      return myObj.id === Number(id)
    });
  }
}
export abstract class Base {
  abstract last_sent_data: KnockoutObservable<{}>
  abstract serialize: KnockoutObservable<{}>
  modified: KnockoutComputed<{}> = ko.computed(() => { return false })
  differences: KnockoutComputed<string[]>
  save() {
    this.last_sent_data(this.serialize())
  }
  constructor() {
  }
  init = (): void => {
    this.differences = ko.computed(() => {
      return diff.getDiff(this.serialize(), this.last_sent_data())
    })
    this.modified = ko.computed(() => {
      let difference = this.differences()
      if (!this.last_sent_data()) {
        return false
      }
      return Object.keys(difference).length > 0
    })
  }

}

export interface FileDownloadInterface {
  file_download: string
}
export abstract class Post extends Base {
  abstract id: KnockoutObservable<number>;
  abstract serialize: KnockoutObservable<{}>
  abstract set(result: any): void
  abstract url: string
  file_download: KnockoutObservable<string> = ko.observable()
  public post(h: any, event: Event, data_object?: any, url?: string) {
    // Abstract class for posting data. Will use PUT if id > 0
    // Also handles buttons
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let data = data_object || this.serialize()
    if (this.id() >= 0) {
      method = HTTPVerbs.put
    } else {
      delete data['id']
      method = HTTPVerbs.post
    }
    return $.ajax({
      url: url || this.url,
      type: method,
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
    }).fail((result, a, c) => {
      console.log(result.responseJSON.errors)
    }).always(function(result) {
      btn.button('reset')
    })
  }
  get_form_and_open(target: string = 'VarmeDokPDF') {
    let importantStuff = window.open('', target);
    importantStuff.document.write('Henter skjema...');
    return this.get_form().done((result: FileDownloadInterface) => {
      importantStuff.location.href = result.file_download;
    })
  }
  get_form() {
    return $.get(this.url, { id: this.id() })
      .done((result: FileDownloadInterface) => {
        this.file_download(result.file_download)
      })
  }
  constructor() { super() }
}
