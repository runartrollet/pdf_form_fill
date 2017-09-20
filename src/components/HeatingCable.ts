import { Post, ObsMod } from "./Common"
import { HeatingCableList } from "./HeatingCableList"
import {
  TSProductModel,
  ProductInterface,
  ProductFilter,
} from "./ProductModel"
let moment = require('moment')
import 'moment/locale/nb';
moment.locale('nb')
// import BootstrapV3DatetimePicker = require("eonasdan-bootstrap-datetimepicker")
require("eonasdan-bootstrap-datetimepicker")
// import * as datepicker from 'bootstrap-datepicker'


ko.bindingHandlers.dateTimePicker = {
  init: function(element, valueAccessor, allBindingsAccessor) {
    // initialize datepicker with some optional options
    var options = allBindingsAccessor!().dateTimePickerOptions || {};

    let default_options = {
      format: "L",
      useCurrent: false,
      calendarWeeks: true,
      showTodayButton: true,
      maxDate: '2030-12-30',
      ignoreReadonly: true,
      tooltips: {
        today: 'Gå til i dag',
        clear: 'Nullstill',
        close: 'Lukk',
        selectMonth: 'Velg måned',
        prevMonth: 'Forrige måned',
        nextMonth: 'Neste måned',
        selectYear: 'Velg år',
        prevYear: 'Forrige år',
        nextYear: 'Neste år',
        selectDecade: 'Velg tiår',
        prevDecade: 'Forrige tiår',
        nextDecade: 'Neste tiår',
        prevCentury: 'Forrige tiår',
        nextCentury: 'Neste tiår',
        incrementHour: 'Øk med en time',
        pickHour: 'Velg time',
        decrementHour: 'Reduser med en time',
        incrementMinute: 'Øk med et minutt',
        pickMinute: 'Velg minutt',
        decrementMinute: 'Reduser med et minutt',
        incrementSecond: 'Øk med et sekund',
        pickSecond: 'Velg sekund',
        decrementSecond: 'Reduser med en sekund',
      }
    }
    $(element).datetimepicker(default_options);

    //when a user changes the date, update the view model
    ko.utils.registerEventHandler(element, "dp.change", function(event: any) {
      var value = valueAccessor();
      if (ko.isObservable(value)) {
        if (event.date === false) {
          value(null);
        } else {
          value(event.date.toDate());
        }
      }
    });

    ko.utils.domNodeDisposal.addDisposeCallback(element, function() {
      var picker = $(element).data("DateTimePicker");
      if (picker) {
        picker.destroy();
      }
    });
  },
  update: function(element, valueAccessor, allBindings, viewModel, bindingContext) {

    var picker = $(element).data("DateTimePicker");
    var minDate = allBindings!().minDate;
    //when the view model is updated, update the widget
    if (picker) {
      if (minDate) {
        picker.minDate(minDate())
      }
      var koDate = ko.utils.unwrapObservable(valueAccessor());

      //in case return from server datetime i am get in this form for example /Date(93989393)/ then fomat this
      koDate = (typeof (koDate) !== 'object') ? new Date(parseFloat(koDate.replace(/[^0-9]/g, ''))) : koDate;

      picker.date(koDate);
    }
  }
};


export interface HeatingCableInterface {
  id: number
  product_id: number
  room_id?: number
  c_date?: Date
  m_date?: Date
  mod_id?: number
  specs: HeatingCableSpecs
}

interface PostInterface {
  url: string
  post(): void;
  serialize(): {}
}

interface MeasurementInterface {
  ohm: number
  mohm: number
  date: Date | null | string
}

interface MeasurementsInterface {
  // TODO: This should be split into seperate interfaces
  install: MeasurementInterface
  pour: MeasurementInterface
  connect: MeasurementInterface
}
interface CalculationsInterface {
  cc?: number
  area_output?: number
}
export interface HeatingCableSpecs {
  measurements?: MeasurementsInterface
  cc: InputReadOnlyToggleInterface
  area_output: InputReadOnlyToggleInterface
}

interface InputReadOnlyToggleInterface {
  v: any
  m: boolean
}

class Measurement {
  ohm: KnockoutObservable<number>
  mohm: KnockoutObservable<number>
  date: KnockoutObservable<Date | string>
  mimmick: KnockoutObservable<boolean>
  mimmickTarget: KnockoutObservable<Measurement>
  serialize: KnockoutComputed<MeasurementInterface>
  constructor(
    modification_observable: any,
    mimmick?: KnockoutObservable<boolean>,
    mimmickTarget?: KnockoutObservable<Measurement>
  ) {
    this.ohm = <ObsMod<number>>modification_observable();
    this.mohm = <ObsMod<number>>modification_observable();
    this.date = <ObsMod<string>>modification_observable(null);
    if (mimmick && mimmickTarget) {
      this.mimmick = mimmick
      this.mimmickTarget = mimmickTarget
    }
    this.serialize = ko.computed(() => {
      let date;
      if (this.date() instanceof Date) {
        date = moment(this.date()).format("YYYY-MM-DD")
      }
      let ohm = this.ohm()
      let mohm = this.mohm()
      if (this.mimmick && this.mimmick() && this.mimmickTarget) {
        ohm = this.mimmickTarget().ohm()
        mohm = this.mimmickTarget().mohm()
      }
      let data = {
        ohm: ohm,
        mohm: mohm,
        date: date
      }
      return data
    })
  }
  set(measurement: MeasurementInterface) {
    if (!measurement) {
      return null
    }
    let date = measurement.date
    if (typeof date === 'string' || date instanceof String) {
      date = new Date(date) // TS-linter complaints this is not a string. It is.
    }
    this.ohm(measurement.ohm)
    this.mohm(measurement.mohm)
    this.date(date)
  }
}

class InputReadOnlyToggle {
  override: ObsMod<boolean>
  calculated: KnockoutComputed<any>
  output: ObsMod<any>
  serialize: KnockoutObservable<InputReadOnlyToggleInterface>
  user_input = <KnockoutObservable<number>>ko.observable();

  constructor(calculateFunction: (() => number), modification_observable: any) {
    this.override = <ObsMod<boolean>>modification_observable(false);
    this.calculated = ko.computed(calculateFunction);
    this.output = modification_observable(() => {
      return Number(this.override() ? this.user_input() : this.calculated())
    }, ko.computed);
    // this.calculated = ko.computed(calculateFunction)
    this.serialize = ko.computed((): InputReadOnlyToggleInterface => {
      return {
        v: this.output() || 0,
        m: this.override(),
      }
    })
    ko.computed(() => {
      if (!this.override()) {
        this.user_input(this.calculated().toFixed(1))
      }
    })
  }
}


export class HeatingCable extends Post {
  measurements_modifications_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()
  product_modifications_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()
  other_modifications_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()

  measurements_observer = (value?: any, kind: any = ko.observable, ) => {
    return this.obs_mod([this.measurements_modifications_list], kind, value);
  }
  other_observer = (value?: any, kind: any = ko.observable) => {
    return this.obs_mod([this.other_modifications_list], kind, value);
  }
  product_observer = (value?: any, kind: any = ko.observable, ) => {
    return this.obs_mod([this.product_modifications_list], kind, value);
  }
  product_id = <ObsMod<number>>this.product_observer();
  url = '/json/v1/heat/'
  id: KnockoutObservable<number> = ko.observable();
  fill_measurement_smartly: KnockoutObservable<boolean> = this.measurements_observer(true)
  measurement_install = ko.observable(new Measurement(this.measurements_observer))
  measurement_pour = ko.observable(new Measurement(
    this.measurements_observer,
    this.fill_measurement_smartly,
    this.measurement_install
  ))
  measurement_connect = ko.observable(new Measurement(
    this.measurements_observer,
    this.fill_measurement_smartly,
    this.measurement_install
  ))
  area_output: KnockoutObservable<InputReadOnlyToggle>
  cc: KnockoutObservable<InputReadOnlyToggle>


  product_model: TSProductModel
  product_filter: KnockoutObservable<ProductFilter>
  suggested_effect: KnockoutComputed<number>;

  validationModel = ko.validatedObservable({
    product_id: this.product_id,
  })
  serialize: KnockoutObservable<HeatingCableInterface>
  constructor(
    product_model: TSProductModel,
    parent: HeatingCableList,
    heating_cable_?: HeatingCableInterface
  ) {
    super(parent)
    let room = parent.parent
    let customer = room.parent.parent
    this.form_url = `${this.form_url}${customer.id()}/${room.id()}/`

    let default_measurement: MeasurementInterface = {
      ohm: 0,
      mohm: 999,
      date: ''
    }
    let default_data: HeatingCableInterface = {
      id: -1,
      product_id: -1,
      specs: {
        measurements: {
          install: default_measurement,
          pour: default_measurement,
          connect: default_measurement
        },
        cc: {
          v: 0,
          m: false
        },
        area_output: {
          v: 0,
          m: false
        },
      }
    }
    let heating_cable = Object.assign(default_data, heating_cable_)
    this.product_id.extend(
      { required: true, number: true, min: 1000000, max: 9999999 })
    this.product_model = product_model
    this.product_filter = ko.observable(new ProductFilter(this, this.parent.parent, this.product_model))

    this.area_output = ko.observable(new InputReadOnlyToggle(() => {
      if (this.product()) {
        if (this.product()!.type == 'mat') {
          return this.product()!.mainSpec
        }
      }
      let heated_area = this.parent.parent.heated_area()
      let room_effect = this.parent.parent.room_effect()
      if (room_effect && heated_area) {
        return parseFloat((room_effect / heated_area).toFixed(1))
      }
      return Number(heating_cable!.specs.area_output.v) || 0
    }, this.other_observer))
    this.cc = ko.observable(new InputReadOnlyToggle(() => {
      if (this.product() && this.product()!.type != 'mat') {
        // For rooms with multiple cables, we need to do some guesswork to
        // calculate the area that this cable is covering.
        let room_effect = this.parent.parent.room_effect()
        let this_effect = this.product()!.effect
        if (room_effect && this_effect) {
          let coverage_fraction = this_effect / room_effect
          let heated_area = this.parent.parent.heated_area()
          let heated_area_of_this_cable = heated_area * coverage_fraction
          let length = this.product()!.specs!.Length
          if (length && heated_area_of_this_cable) {
            let value = heated_area_of_this_cable / length * 100
            return parseFloat(value.toFixed(1))
          }
        }
      }
      // Set an initial value, to keep the modified-flag from raising
      return Number(heating_cable!.specs.cc.v) || 0
    }, this.other_observer))

    this.serialize = ko.computed(() => {

      let obj: HeatingCableInterface = {
        id: this.id(),
        room_id: this.parent.parent.id(),
        product_id: Number(this.product_id()),
        specs: {
          measurements: {
            install: this.measurement_install().serialize(),
            pour: this.measurement_pour().serialize(),
            connect: this.measurement_connect().serialize()
          },
          cc: this.cc().serialize(),
          area_output: this.area_output().serialize()
        },
      }
      return obj
    })
    this.suggested_effect = ko.computed(() => {
      let this_effect = 0
      if (this.product()) {
        this_effect = this.product()!.effect
      }
      return this.parent.parent.bestFitEffect() - (this.parent.parent.room_effect() - this_effect)
    })
    this.set(heating_cable)
  }
  bindDatePicker() {
    // $('.datepicker').datepicker({
    // useCurrent: false
    // })
  }
  product = ko.computed((): ProductInterface | undefined => {
    if (this.product_id() >= 0 && this.product_model) {
      return this.product_model.by_id(this.product_id())

    }
  })


  set(heating_cable: HeatingCableInterface) {
    this.id(heating_cable.id)
    this.product_id(Number(heating_cable.product_id))
    if (heating_cable.specs && heating_cable.specs.measurements) {
      // The order in which we set these matters. (minDate)
      this.measurement_connect().set(heating_cable.specs.measurements.connect)
      this.measurement_pour().set(heating_cable.specs.measurements.pour)
      this.measurement_install().set(heating_cable.specs.measurements.install)

      this.area_output().override(Boolean(heating_cable.specs.area_output!.m))
      this.area_output().user_input(Number(heating_cable.specs.area_output!.v))
      this.cc().override(Boolean(heating_cable.specs.cc!.m))
      this.cc().user_input(Number(heating_cable.specs.cc!.v))
    }
    if (this.serialize) {
      this.save()
    }
    let fill_measurement_smartly = (
      this.measurement_install().ohm() === this.measurement_pour().ohm() &&
      this.measurement_install().ohm() === this.measurement_connect().ohm() &&
      this.measurement_install().mohm() === this.measurement_pour().mohm() &&
      this.measurement_install().mohm() === this.measurement_connect().mohm()
    )
    this.fill_measurement_smartly(fill_measurement_smartly)
    this.fill_measurement_smartly.save()
  }
  modifications_other = ko.computed(() => {
    return this.modification_check(this.other_modifications_list())
  })
  product_modifications = ko.computed(() => {
    return this.modification_check(this.product_modifications_list())
  })
  measurements_modifications = ko.computed(() => {
    return this.modification_check(this.measurements_modifications_list())
  })



}
