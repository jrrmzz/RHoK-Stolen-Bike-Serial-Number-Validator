require 'geokit'

class Bike
  include DataMapper::Resource
  property :serial, String, :key => true
  property :color, String
  property :make, String
  property :model_name, String # ":model" is reserved
  property :lat, Float
  property :lng, Float
  
  def location=(address)
    geocode = Geokit::Geocoders::YahooGeocoder.geocode address
    self.lat = geocode.lat
    self.lng = geocode.lng
  end
end
