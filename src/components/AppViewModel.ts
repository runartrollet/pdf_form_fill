import { TSProductModel } from './ProductModel'
import { RoomInterface, Rooms} from './InterfaceRoom'
import nb_NO = require('./../../node_modules/knockout.validation/localization/nb-NO.js')
import kv = require("knockout.validation");
import { StrIndex } from "./Common"
import ko = require("knockout");
import $ = require("jquery");
var titleCase = require('title-case')

require("knockout.typeahead");
require("knockout-template-loader?name=suggestion-template!html-loader?-minimize!./suggestion.html");

// Switch locale for knockout.validation
kv.defineLocale('no-NO', nb_NO);
kv.locale('nb-NO')

interface AddressInterface {
  post_area: string;
  post_code: number;
  street_name: string;
}

interface AddressFullInterface extends AddressInterface{
  address1: string;
  address2: string;
}
interface RoomSpecsInterface {
  area: number;
  heated_area: number;
  outside: boolean;
}
interface RoomInterface {
  name: string;
  id: number;
  specs: RoomSpecsInterface;
}
interface CustomerInterface {
    id: number;
    name: string;
    address: AddressFullInterface;
    rooms: RoomInterface[];
}

interface UserFormInterface {
  date: string;
  id: number;
  request_form: RequestFormInterface
}

interface RequestFormInterface {
  anleggs_adresse: string
  anleggs_adresse2: string
  anleggs_postnummer: number
  anleggs_poststed: string
  rom_navn: string
  areal: number
  oppvarmet_areal: number
  selected_vk: number
  product_id: number
  address_id: number
  ohm_a: number
  ohm_b: number
  ohm_c: number
  mohm_a: boolean
  mohm_b: boolean
  mohm_c: boolean
}

interface FileDownloadInterface {
  address_id: number
  file_download: string
  filled_form_modified_id: number
  error_fields?: Array<string>
  error_message?: string
}


export class TSAppViewModel {
  anleggs_adresse: KnockoutObservable<{}> = ko.observable().extend({
    required: true,
    minLength: 3,
    maxLength: 50
  })
  anleggs_adresse2: KnockoutObservable<{}> = ko.observable().extend({
    required: false,
    minLength: 3,
    maxLength: 50
  })
  anleggs_poststed: KnockoutObservable<{}> = ko.observable().extend({
    required: true,
    minLength: 3,
    maxLength: 50
  });
  anleggs_postnummer: KnockoutObservable<{}> = ko.observable().extend({
    required: true,
    minLength: 4,
    number: true,
    min: 1000,
    max: 9999,
  });
  manufacturor: KnockoutObservable<string> = ko.observable();
  vk_type: KnockoutObservable<string> = ko.observable();
  mainSpec: KnockoutObservable<number> = ko.observable();
  rom_navn: KnockoutObservable<{}> = ko.observable().extend({
    required: true,
    minLength: 2,
    maxLength: 50
  });
  outside: KnockoutObservable<boolean> = ko.observable();
  areal: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0.1
  });
  oppvarmet_areal: KnockoutObservable<{}> = ko.observable().extend({
    required: true,
    number: true,
    min: 0.1
  });
  effect: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
  });
  ohm_a: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0,
    max: 1000,
  });
  ohm_b: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0,
    max: 1000,
  });
  ohm_c: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0,
    max: 1000,
  });
  mohm_a: KnockoutObservable<{}> = ko.observable();
  mohm_b: KnockoutObservable<{}> = ko.observable();
  mohm_c: KnockoutObservable<{}> = ko.observable();
  error_fields: KnockoutObservableArray<string> = ko.observableArray();
  error_message: KnockoutObservable<string> = ko.observable();
  file_download: KnockoutObservable<string> = ko.observable();
  last_sent_args: KnockoutObservable<string> = ko.observable();
  form_args: KnockoutObservable<string> = ko.observable($('#form').serialize());
  Products: KnockoutObservable<TSProductModel> = ko.observable();
  selected_vk: KnockoutObservable<number> = ko.observable();
  forced_selected_vk: KnockoutObservable<number> = ko.observable();
  address_id: KnockoutObservable<number> = ko.observable();
  customer_id: KnockoutObservable<number> = ko.observable();
  rooms: KnockoutObservableArray<RoomInterface> = ko.observableArray();
  room_id: KnockoutObservable<number> = ko.observable();
  filled_form_modified_id: KnockoutObservable<number> = ko.observable();
  user_forms: KnockoutObservableArray<string> = ko.observableArray();
  company_forms: KnockoutObservableArray<string> = ko.observableArray();
  validation_errors: KnockoutValidationErrors = kv.group(self);
  loading: KnockoutObservableArray<string> = ko.observableArray();
  autocompleteAddress: KnockoutComputed<string>;

  delete: KnockoutObservable<string> = ko.observable();


  noname: any

  constructor() {
    kv.init({
      decorateInputElement: true,
      errorElementClass: 'has-error has-feedback',
      // successElementClass: 'has-feedback has-success',
      insertMessages: true,
      // decorateElement: true,
      // errorElementClass: 'error',
      errorMessageClass: 'bg-danger'
    });

    // Add bootstrap-validation-css to parent of field
    let init = ko.bindingHandlers['validationCore'].init!;
    ko.bindingHandlers['validationCore'].init = (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) => {
      init(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);
      let config = kv.utils.getConfigOptions(element);
      // if requested, add binding to decorate element
      if (config.decorateInputElement && kv.utils.isValidatable(valueAccessor())) {
        let parent = $(element).parent();
        if (parent.length) {
          ko.applyBindingsToNode(parent[0], {
            validationElement: valueAccessor()
          });
        }
      }
    };
    this.Products(new TSProductModel(this));
    this.Products().getProducts();

    this.noname = ko.computed(() => {
      try {
        var f = this.Products().flat_products();
        if (f.length > 0) {
          this.get_user_forms();
        }
      } catch (e) {

      } finally {

      }
    });

    this.autocompleteAddress = ko.computed(() => {
      let url: string = '/address/?q=%QUERY'
      if (this.anleggs_postnummer()) {
        url += '&p=' + this.anleggs_postnummer()
      }
      return url
      // We need a rateLimiter here so that the url doesn't change too early
      // when a user clicks a selection.
    }).extend({ rateLimit: 50 })


    ko.computed(() => {
      if (this.mainSpec()) {
        try {
          let f = this.Products().spec_groups();
          if (f.find(item => item.mainSpec === this.mainSpec())) {

          }
          if (this.findWithAttr(f, 'mainSpec', this.mainSpec()) < 0) {
            this.mainSpec(null);
          }
        } catch (e) {

        } finally {

        }
      }
    });

    $.get("/json/v1/customer/", {id: 51})
    .done((result: CustomerInterface) => {
      this.anleggs_adresse(result.address.address1)
      this.anleggs_adresse2(result.address.address2)
      this.anleggs_postnummer(result.address.post_code)
      this.anleggs_poststed(result.address.post_area)
      this.customer_id(result.id)
      this.rooms(result.rooms)
      console.log(result)
    })
  }

  suggestRoom = () => {
    let listOfRooms: RoomInterface[] = []
    Rooms.forEach((room, index) => {
      listOfRooms.push({
        name: room.name,
        id: index
      })
      if (room.aliases) {
        for (let alias of room.aliases) {
          listOfRooms.push({
            name: alias,
            id: index
          })
        }
      }
    })
    return listOfRooms
  };

  roomSuggestionOnSelect = (
    value: KnockoutObservable<string>,
    room: RoomInterface) => {
    let roomObject = Rooms[room.id]
    this.outside(<boolean>(roomObject.outside));

  }

  suggestionOnSelect = (
    value: KnockoutObservable<{}>,
    address: AddressInterface) => {
    value(titleCase(address.street_name))
    this.anleggs_postnummer(address.post_code)
    this.anleggs_poststed(address.post_area.toUpperCase())
  }

  form_changed = ko.computed(() => {
    return this.form_args() !== this.last_sent_args();
  }, this);

  parse_form_download = (result: FileDownloadInterface) => {
    this.last_sent_args(this.form_args());
    if (result.error_fields) {
      this.error_fields(result.error_fields);
    }
    if (result.file_download) {
      this.file_download(result.file_download);
      if (result.address_id) {
        this.address_id(result.address_id);
      }
      if (result.filled_form_modified_id) {
        this.filled_form_modified_id(result.filled_form_modified_id);
      }
    }
    if (result.error_message) {
      this.error_message(result.error_message);
    }
  }
  post_customer_form = (e: any, event: any) => {
    let button = $(event.target)
    button.button('loading')
    let type = 'POST'
    let data = $('#customer_form').serializeArray()
    if (this.customer_id()){
      data.push({name: 'id', value: String(this.customer_id())})
    }
    if (this.customer_id()) {
      type = 'PUT'
    }
    $.ajax({
      url: '/json/v1/customer/',
      type: type,
      data: data
    }).done((result) => {
      this.customer_id(result.customer_id)
      setTimeout(() => {
        button.text('Endre')
      }, 20)
    }).always(() => {
      button.button('reset')
    })
  }
  post_room_form = (e: any, event: any) => {
    let button = $(event.target)
    button.button('loading')
    let type = 'POST'
    let data = $('#room_form').serializeArray()
    if (this.customer_id()) {
      data.push({name: 'customer_id', value: String(this.customer_id())})
    }
    if (this.room_id()) {
      console.log(this.room_id())
      data.push({name: 'room_id', value: String(this.room_id())})
    }
    if (this.room_id()) {
      type = 'PUT'
    }
    if (this.customer_id()) {
      $.ajax({
        url: '/json/v1/room/',
        type: type,
        data: data
      }).done((result) => {
        this.room_id(result.room_id)
        setTimeout(() => {
          button.text('Endre')
        }, 20)
      }).always(() => {
        button.button('reset')
      })
    }
  }

  post_form = () => {
    this.form_args($('#form').serialize());
    if (this.validation_errors().length > 0) {
      this.validation_errors.showAllMessages();
      return false;
    }
    if (this.form_changed() || !this.filled_form_modified_id()) {
      this.file_download(null);
      this.loading.push('fill_form');
      $.post("/json/heating/", {
        'anleggs_adresse': this.anleggs_adresse(),
        'anleggs_poststed': this.anleggs_poststed(),
        'anleggs_postnummer': this.anleggs_postnummer(),
        'rom_navn': this.rom_navn(),
        'areal': this.areal(),
        'oppvarmet_areal': this.oppvarmet_areal(),
        'mohm_a': this.mohm_a(),
        'mohm_b': this.mohm_b(),
        'mohm_c': this.mohm_c(),
        'ohm_a': this.ohm_a(),
        'ohm_b': this.ohm_b(),
        'ohm_c': this.ohm_c(),
        'product_id': this.selected_vk(),
        'address_id': this.address_id(),
        'filled_form_modified_id': this.filled_form_modified_id()
      })
        .done((result: FileDownloadInterface) => {
          this.loading.remove('fill_form');
          this.parse_form_download(result);
        });
    } else {
      this.loading.push('fill_form');
      $.get("/json/heating/", {
        'filled_form_modified_id': this.filled_form_modified_id()
      }).done((result: FileDownloadInterface) => {
        this.loading.remove('fill_form');
        this.parse_form_download(result);
      });
    }
  };
  findWithAttr = (array: Array<any>, attr: string, value: any) => {
    for (var i = 0; i < array.length; i += 1) {
      if (array[i][attr] === value) {
        return i;
      }
    }
    return -1;
  }

  get_user_forms = () => {
    this.loading.push('user_form')
    $.get("/forms.json", {})
      .done((result) => {
        result.user_forms.prefix = 'user_forms';
        result.company_forms.prefix = 'company_forms';
        this.user_forms(result.user_forms);
        this.company_forms(result.company_forms);
        this.loading.remove('user_form')
      });
  }

  get_product_by_id = (id: number) => {
    let f = this.Products().flat_products();
    return f.find(myObj => myObj.id === Number(id));
  }

  confirmed_delete = (e: UserFormInterface) => {
    this.delete('');
    this.loading.push('delete');
    $.ajax({
      url: 'json/form_mod/' + e.id,
      type: 'DELETE',
      data: {
        id: e.id
      }
    })
      .done((result) => {
        this.loading.remove('delete');
        this.get_user_forms();
      });
  };

  edit_form = (e: UserFormInterface) => {
    var f = e.request_form;
    this.filled_form_modified_id(e.id);
    this.anleggs_adresse(f.anleggs_adresse);
    this.anleggs_postnummer(f.anleggs_postnummer);
    this.anleggs_poststed(f.anleggs_poststed);
    this.rom_navn(f.rom_navn);
    this.areal(f.areal);
    this.oppvarmet_areal(f.oppvarmet_areal);
    this.selected_vk(f.product_id);
    // this.address_id(e.address_id);
    // TODO: fix address_id
    this.ohm_a(f.ohm_a);
    this.ohm_b(f.ohm_b);
    this.ohm_c(f.ohm_c);
    this.mohm_a(f.mohm_a);
    this.mohm_b(f.ohm_b);
    this.mohm_c(f.ohm_c);
    this.last_sent_args($('#form').serialize());
    this.form_args($('#form').serialize());
    ($('.nav-tabs a[href="#main_form"]') as any).tab('show');
  };

}
// Inject our CSRF token into our AJAX request.
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
    }
  }
})
