import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-text-classification',
  templateUrl: './text-classification.component.html',
  styleUrls: ['./text-classification.component.scss']
})
export class TextClassificationComponent implements OnInit {

  text = 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Fugit eius,\n consequatur earum blanditiis doloremque molestiae corrupti quos ipsum temporibus aut, atque sequi quidem quam vel.\n\n Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?Aliquid excepturi incidunt dignissimos eius?'
  selected = ''

  classes = [
    {label: 'Limit change'},
    {label: 'Movement'},
    {label: 'Meeting'},
  ]


  constructor() { }

  ngOnInit(): void {
  }

  select(cls: string) {
    this.selected = cls
    console.log(this.selected)
  }

}
