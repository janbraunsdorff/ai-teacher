import { Component, ElementRef, Input, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { Subject } from 'rxjs';
import { Value } from 'src/app/tasks/text-entity-registration/text-entity-registration.component';

@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'app-text',
  templateUrl: './text.component.html',
  styleUrls: ['./text.component.scss']
})
export class TextComponent implements OnInit {
  
  @Input('text') text:string = '';
  @Input('selection') selection: Subject<Value> | null = null

  @ViewChild('text_wrapper') textWrapper: ElementRef | null;

  constructor() { }

  ngOnInit(): void {
  }

  get_selected() {
    const selection = window.getSelection();
    if (selection == null) {
      return
    }

    const textSeleted = selection.toString();
    if (textSeleted == null || textSeleted == '') {
      return
    }

    const selectionRange = selection.getRangeAt(0);
    const range = selectionRange.cloneRange();

    console.log(selectionRange.startOffset + " -> " + selectionRange.endOffset + " " + textSeleted)


    const marker = document.createElement('span');
    marker.classList.add('selected-text-xyz');

    range.surroundContents(marker);

    console.log(this.textWrapper?.nativeElement.innerHTML)
  }

}
