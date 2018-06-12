import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  name = '';
  lastName = '';
  instagram = '';
  memberSince = '';

  tiles = [
    {text: 'One', cols: 3, rows: 1, color: 'lightblue'},
    {text: 'Two', cols: 1, rows: 2, color: 'lightgreen'},
    {text: 'Three', cols: 1, rows: 1, color: 'lightpink'},
    {text: 'Four', cols: 2, rows: 1, color: '#DDBDF1'},
  ];

  constructor() { }

  ngOnInit() {
    console.log("test");
    // There will be a service call here. Most likely a subscribe.
    this.name = 'Pablo';
    this.lastName = 'Prieto';
    this.instagram = 'instagram.com/Pablo';
    this.memberSince = '06/07/2018';
  }

}
