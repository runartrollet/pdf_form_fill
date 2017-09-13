import { ByID, } from "./Common"
import { HeatingCable, HeatingCableInterface } from "./HeatingCable"
import { Room } from "./Room"
import { TSAppViewModel } from "./AppViewModel"



export class HeatingCableList extends ByID {
  list: KnockoutObservableArray<HeatingCable>
  parent: Room
  root: TSAppViewModel
  constructor(root: TSAppViewModel, parent: Room, heating_cables: HeatingCableInterface[] = []) {
    super([])
    this.parent = parent
    this.root = root
    let heating_cables_objects: HeatingCable[] = []
    if (heating_cables_objects) {
      heating_cables_objects = heating_cables.map((x) => {
        return new HeatingCable(this.root.Products(), this, x)
      })
    }
    this.list(heating_cables_objects)
  }
  add = (event: Event) => {
    let new_heating_cable = this.by_id(-1)
    if (!new_heating_cable) {
      this.list.push(new HeatingCable(this.root.Products(), this))
    }
    this.root.editing_heating_cable_id(-1)
    setTimeout(() => {    // Expand the panel
      let btn = $(event.target)
      let accordian = $('#accordion-heat')
      let panel = accordian.find('#heat-1')
      let panel_vk = panel.find('#panel_select_cable-1')
      panel.collapse('show')
      panel_vk.addClass('in')
    }, 20)

  }
}
