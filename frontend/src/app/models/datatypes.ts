export interface Segements {
    label: string;
    id: string
    segements:  Segement[];
    value?: string
  }
  
export interface Segement {
    start: Point;
    end: Point;
}
  
interface Point {
    x: number;
    y: number;
  }
  