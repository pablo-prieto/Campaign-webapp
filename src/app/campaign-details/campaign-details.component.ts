import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { Campaign } from '../models/campaign';

@Component({
  selector: 'app-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.css']
})
export class CampaignDetailsComponent implements OnInit {

  campaign: Campaign;
  id: string;
  private sub: any;
  img: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit() {
    // this.hero$ = this.route.paramMap.pipe(
    //   switchMap((params: ParamMap) =>
    //     this.service.getHero(params.get('id')))
    // );
    this.sub = this.route.params.subscribe(params => {
      this.id = params['id'];

      // In a real app: dispatch action to load the details here.
    });
    this.img = "https://material.angular.io/assets/img/examples/shiba2.jpg";
  }

}
