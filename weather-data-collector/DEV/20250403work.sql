SELECT * FROM [KH16].[dbo].[TB_ULTRASRTNCST]

select count(*) from weather_data

select * from weather_data order by EXEC_Date desc

select BASE_DATE, BASE_TIME, category, COUNT(VALUE) AS CNT
from weather_data 
WHERE BASE_DATE = '20250403'
GROUP BY BASE_DATE, BASE_TIME, category
--HAVING COUNT(VALUE) <= 1
ORDER BY BASE_DATE, BASE_TIME, category

select * from weather_data 
WHERE BASE_DATE = '20250403'
AND BASE_TIME = '1300'
AND CATEGORY = 'VEC'
order by exec_date desc

select BASE_DATE, BASE_TIME, category, VALUE
from weather_data 
WHERE BASE_DATE = '20250403'
AND BASE_TIME = '1300'
GROUP BY BASE_DATE, BASE_TIME, category, VALUE
--HAVING COUNT(VALUE) <= 1
ORDER BY BASE_DATE, BASE_TIME, category, VALUE

- 풍속 정보
동서바람성분(UUU) : 동(+표기), 서(-표기)
남북바람성분(VVV) : 북(+표기), 남(-표기)


초단기실황	
	T1H	기온	℃	10
	RN1	1시간 강수량	mm	8
	UUU	동서바람성분	m/s	12
	VVV	남북바람성분	m/s	12
	REH	습도	%	8
	PTY	강수형태	코드값	4
	VEC	풍향	deg	10
	WSD	풍속	m/s	10

풍향
- 풍향 구간별 표현단위
풍향 구간(°)	표현 단위	풍향 구간(°)	표현 단위
0 – 45	N-NE	180 – 225	S-SW
45 – 90	NE-E	225 – 270	SW-W
90 – 135	E-SE	270 – 315	W-NW
135 – 180	SE-S	315 – 360	NW-N

