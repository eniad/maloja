import urllib
from datetime import datetime, timedelta
import database
from utilities import clock

from htmlmodules import module_scrobblelist, module_pulse, module_artistcharts_tiles, module_trackcharts_tiles

		
def instructions(keys):

	# get start of week
	tod = datetime.utcnow()
	change = (tod.weekday() + 1) % 7
	d = timedelta(days=change)
	newdate = tod - d
	weekstart = [newdate.year,newdate.month,newdate.day]

	clock()

	# artists
	
	topartists_total = module_artistcharts_tiles()
	topartists_year = module_artistcharts_tiles(since="year")
	topartists_month = module_artistcharts_tiles(since="month")
	topartists_week = module_artistcharts_tiles(since=weekstart)
	
	clock("Artists")

	# tracks
	
	toptracks_total = module_trackcharts_tiles()
	toptracks_year = module_trackcharts_tiles(since="year")
	toptracks_month = module_trackcharts_tiles(since="month")
	toptracks_week = module_trackcharts_tiles(since=weekstart)
	
	
	clock("Tracks")


	# scrobbles
	html_scrobbles, _, _ = module_scrobblelist(max_=15,shortTimeDesc=True,pictures=True)
	
	clock("Scrobbles")
	
	# stats
	amount = database.get_scrobbles_num(since="today")
	scrobbles_today = "<a href='/scrobbles?since=today'>" + str(amount) + "</a>"
	
	amount = database.get_scrobbles_num(since="month")
	scrobbles_month = "<a href='/scrobbles?since=month'>" + str(amount) + "</a>"

	amount = database.get_scrobbles_num(since="year")
	scrobbles_year = "<a href='/scrobbles?since=year'>" + str(amount) + "</a>"

	amount = database.get_scrobbles_num()
	scrobbles_total = "<a href='/scrobbles'>" + str(amount) + "</a>"
	
	
	clock("Amounts")
	
	# pulse
	dt = datetime.utcnow()
	first_month = [dt.year-1,dt.month+1]
	dt_firstweek = dt - timedelta(11*7) - timedelta((6-dt.weekday()))
	first_week = [dt_firstweek.year,dt_firstweek.month,dt_firstweek.day]
	dt_firstday = dt - timedelta(6)
	first_day = [dt_firstday.year,dt_firstday.month,dt_firstday.day]
	first_year = [dt.year - 9]
	if first_month[1] > 12: first_month = [first_month[0]+1,first_month[1]-12]
	
	html_pulse_days = module_pulse(max_=7,since=first_day,step="day",trail=1)
	html_pulse_weeks = module_pulse(max_=12,since=first_week,step="week",trail=1)
	html_pulse_months = module_pulse(max_=12,since=first_month,step="month",trail=1)	
	html_pulse_years = module_pulse(max_=10,since=first_year,step="year",trail=1)
	
	
	#html_pulse_week = module_pulse(max_=7,since=weekstart,step="day",trail=1)
	#html_pulse_month = module_pulse(max_=30,since=[dt.year,dt.month],step="day",trail=1)
	#html_pulse_year = module_pulse(max_=12,since=[dt.year],step="month",trail=1)

	clock("Pulse")

	#pushresources = [{"file":img,"type":"image"} for img in artistimages + trackimages] #can't push scrobble images as we don't get them from the module function, need to think about that
	pushresources = []

	replace = {
#	"KEY_ARTISTIMAGE":artistimages,"KEY_ARTISTNAME":artisttitles,"KEY_ARTISTLINK":artistlinks,"KEY_POSITION_ARTIST":posrange,
#	"KEY_TRACKIMAGE":trackimages,"KEY_TRACKNAME":tracktitles,"KEY_TRACKLINK":tracklinks,"KEY_POSITION_TRACK":posrange,
	"KEY_TOPARTISTS_TOTAL":topartists_total,"KEY_TOPARTISTS_YEAR":topartists_year,"KEY_TOPARTISTS_MONTH":topartists_month,"KEY_TOPARTISTS_WEEK":topartists_week,
	"KEY_TOPTRACKS_TOTAL":toptracks_total,"KEY_TOPTRACKS_YEAR":toptracks_year,"KEY_TOPTRACKS_MONTH":toptracks_month,"KEY_TOPTRACKS_WEEK":toptracks_week,
	"KEY_SCROBBLES_TODAY":scrobbles_today,"KEY_SCROBBLES_MONTH":scrobbles_month,"KEY_SCROBBLES_YEAR":scrobbles_year,"KEY_SCROBBLES_TOTAL":scrobbles_total,
	#"KEY_SCROBBLE_TIME":scrobbletimes,"KEY_SCROBBLE_ARTISTS":scrobbleartists,"KEY_SCROBBLE_TITLE":scrobbletracklinks,"KEY_SCROBBLE_IMAGE":scrobbleimages,
	"KEY_SCROBBLES":html_scrobbles,
	#"KEY_PULSE_TERM":pulse_rangedescs,"KEY_PULSE_AMOUNT":pulse_amounts,"KEY_PULSE_BAR":pulse_bars
	"KEY_PULSE_MONTHS":html_pulse_months,"KEY_PULSE_YEARS":html_pulse_years,"KEY_PULSE_DAYS":html_pulse_days,"KEY_PULSE_WEEKS":html_pulse_weeks,
	#"KEY_PULSE_YEAR":html_pulse_year,"KEY_PULSE_MONTH":html_pulse_month,"KEY_PULSE_WEEK":html_pulse_week
	}
	
	return (replace,pushresources)

