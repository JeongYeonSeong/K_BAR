package Personal;

import java.text.DecimalFormat;
import java.util.Random;
import java.util.Scanner;

public class GYungMa {

	public static void main(String[] args) {
		
		Random ra = new Random();
		DecimalFormat df = new DecimalFormat("#");
		
		double mon = 100000;
		int test = 0;
		String aaa[] = {"0","1","2","3","4","5","6","7","8","9"};
		String hor[] = {"ムシニ","ジョー","ハーヤー","ポロポロ","WAGON","ツイタ","ブルンくん","プロリ","ダラリ"};
		int rate[] = new int [9];
		double rat2[] = {1.1, 1.4, 2.2, 5.4, 11.6, 19.8, 26.0, 46.9, 163.0};
		double race[] = {0,0,0,0,0,0,0,0,0};
		
		int bet = 0;
		int pp =0;
		int compare =0;
		int vic = 0;
		double m;
		int ment = 0;
		int kk =0;
		
		for (int i = 0;i<rate.length;i++) {
			rate[i]=ra.nextInt(99)+1;
			for (int k = 0;k<rate.length;k++) {
				if (i==k)
					continue;
				if (rate[i]==rate[k]) {
					i--;
					break;
				}
			}
		}
		for (int i = 0;i<rate.length;i++) {
			compare = 0;
			for (int k = 0;k<race.length;k++) {
				if (i==k)
					continue;
				if (rate[i]<rate[k]) {
					compare++;
				}
			}
			race[i]=compare;
		}
		for (int i = 0; i<race.length;i++) {
			for (int k = 0; k<9;k++) {
				if (race[k]==i)
					race[k]=rat2[i];
			}
		}
		System.out.println("K Barにようこそ！ \nここでは全てがトップのみのものです。"
				+ "\nスタートキャッシュ : "+df.format(mon)+"円です。"
				+ "\nさあ、始めましょう！！！！");
		while (true) {
			Scanner st = new Scanner(System.in);
			Scanner sc = new Scanner(System.in);
			if (mon <= 0) {
				break;
			}
			int race2[] = {0,0,0,0,0,0,0,0,0};
			ment=0;
			if (test==1) {
				for (int i = 0;i<rate.length;i++) {
					rate[i]=ra.nextInt(99)+1;
					for (int k = 0;k<rate.length;k++) {
						if (i==k)
							continue;
						if (rate[i]==rate[k]) {
							i--;
							break;
						}	
					}
				}
				for (int i = 0;i<rate.length;i++) {
					compare = 0;
					for (int k = 0;k<race.length;k++) {
						if (i==k)
							continue;
						if (rate[i]<rate[k]) {
							compare++;
						}
					}
					race[i]=compare;
				}
				for (int i = 0; i<race.length;i++) {
					for (int k = 0; k<9;k++) {
						if (race[k]==i)
							race[k]=rat2[i];
					}
						
					
				}
				
			}
			System.out.println("****************************************");
			System.out.print("馬の情報を見る 1"+"\nかける 2");
			int p = sc.nextInt();
			if (p==1) {
				test=0;
				System.out.println("****************************************");
				System.out.println("今日の出場情報とコンディション");
				for (int i = 0;i<hor.length;i++) {
					System.out.println( (i+1)+" "+hor[i]+" "+rate[i]);
				}
			}
			if (p==2) {
				test=1;
				System.out.println("****************************************");
				System.out.println("誰にかけますか。");
				kk = sc.nextInt();
				
				while(true) {
				
					if (kk==pp+1) {
						bet=pp;
						System.out.println(hor[pp]+"を選択しました。");
						break;
					}
					else if (pp==hor.length) {
						System.out.println("存在していない馬です。選び直してください。");
						kk = sc.nextInt();
						pp = 0;
					}
					pp++;
				}
				while (true) {
					System.out.println("いくらをかけますか。");
					 m = sc.nextInt();
					if (m>mon) {
						System.out.println("キャッシュが足りないです。");
						continue;
					}else {
						mon-=m;
						break;
					}
				}
				System.out.println(df.format(m)+ "円をかけました。"
						+ "\n配当率は" + race[pp]+ "です。"
						+ "\n試合が始まります。");
				while (true){
					for (int i = 0;i<rate.length;i++) {
						if(ment ==2) {
							System.out.println("全馬、ヨーーーーーイ");
							try {
								Thread.sleep(500);
							}catch (InterruptedException e) {}	
						}
						if(ment ==4) {
							System.out.println("始めました。");
							try {
								Thread.sleep(500);
							}catch (InterruptedException e) {}	
						}
						int rasu = ra.nextInt(200);
						if (rate[i]>rasu) {
							race2[i]+=1;
							if(race2[i]==2)
								System.out.println(hor[i]+"が30パーセント区間を通っています。");
							if(race2[i]==3)
								System.out.println(hor[i]+"が50パーセント区間を通っています。");
							if(race2[i]==5)
								System.out.println(hor[i]+"、最後の一周です。勝利が目の前！！！！");
							if(race2[i]==6) {
								System.out.println(hor[i]+"が決勝線を通りました。");
								vic = i;
								test=0;
								break;
							}
						}
						try {
							Thread.sleep(100);
						}catch (InterruptedException e) {}	
						ment++;
					}
								
					if (test == 0) {
						test=1;
						break;
					}
				
				}
				if (vic ==pp) {
					double pppp = (int)m*race[pp];
					mon = (int)mon+pppp;
					
					System.out.println("あなたの馬が優勝して"+ df.format(pppp)+"を取りました。\nキャッシュ : "+df.format(mon));
					pp = 0;
				}else
					System.out.println("あなたの馬は敗北して"+ (int)m +"を取られてしまいました。\nキャッシュ : "+df.format(mon));
					
				}
			}
			System.out.println("あなたは全てのキャッシュを取られてしまいました。\nまたお金があったらご来場お願いします。");
		
	}

}
