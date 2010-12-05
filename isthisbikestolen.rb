%w( rubygems sinatra datamapper haml erb ).each {|lib| require lib }
Dir['models/*.rb'].each {|model| require model }

configure do
  DataMapper::setup(:default, "sqlite3://#{Dir.pwd}/isthisbikestolen.db")
  DataMapper.auto_upgrade!
end

get '/' do
  redirect '/index.html' # WTF?
end

get '/register' do
  haml :register
end

post '/register' do
  #TODO: report if stolen
  #TODO: report to last owner if duplicate
  # else...
  @bike = Bike.create(params[:bike])
  #TODO: haml :thanks
  redirect '/bikes' #REMOVE
end

get '/thanks' do
  'Thank you for registering' 
end

#FIXME: For testing only 
get '/bikes' do
  haml :bikes
end

get '/bikes.js' do
  @bikes = Bike.all
  erb :'bikes.js'
end


