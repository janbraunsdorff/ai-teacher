import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { TextService } from 'src/app/services/backend/text.service';

@Component({
  selector: 'app-text-entity-registration',
  templateUrl: './text-entity-registration.component.html',
  styleUrls: ['./text-entity-registration.component.scss']
})
export class TextEntityRegistrationComponent implements OnInit {

  selection = new Subject<Value>();

  plain_text = 'Hallo zusammen \n\n Ich bin Blau wie das Meer \n voll wie unser laderaum \n breit so wie die Ärsche von Tortuga \n-------\n Ich bin Blau wie das Meer \n voll wie unser laderaum'
  selected = ''
  action = ''
  activate = ''

  classes: Clazz[] = [
    {id: '001', label: 'Greeting', values: []},
    {id: '002', label: 'Blue', values: []},
    {id: '003', label: 'Red', values: []},
  ]


  constructor(public service: TextService) { }

  ngOnInit(): void {
    this.selection.subscribe(res => {
      if (this.activate == '') {
        return
      }
      let clazz = this.classes.filter(r => r.id == this.activate)
      if (clazz == null){
        return
      }

      clazz[0].values.push(res)

      console.log(this.plain_text.substring(res.start-1, res.end) == res.value);
      console.log(res.value);
      console.log(this.plain_text.substring(res.start-1, res.end))

      this.plain_text = 
        this.plain_text.substring(0, res.start-1) + 
        '</span><span style="color: red">' +  
        this.plain_text.substring(res.start-1, res.end) + 
        '</span><span>' + 
        this.plain_text.substring(res.end+1, this.plain_text.length)   
        
        
      console.log(this.plain_text)
    })
    

  }

  select(cls: string) {
    this.selected = cls
    console.log(this.selected)
  }

  draw(id: string){
    if (this.action != 'draw'){
      this.action = 'draw'
    }else {
      this.action = ''
    }

    if (this.activate != id) {
      this.activate = id
    }else {
      this.activate = ''
    }
  }

}

export interface Clazz{
  id: string
  label: string
  values: Value[]
}

export interface Value {
  start: number
  end: number
  value: string
}