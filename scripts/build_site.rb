#!/usr/bin/env ruby

require "jekyll"
require "optparse"

options = {
  "source" => Dir.pwd,
  "destination" => File.join(Dir.pwd, "_site")
}

OptionParser.new do |parser|
  parser.banner = "Usage: bundle exec ruby scripts/build_site.rb [options]"
  parser.on("--url URL", "Absolute site origin") { |value| options["url"] = value }
  parser.on("--baseurl PATH", "Path below the origin") { |value| options["baseurl"] = value }
  parser.on("--destination PATH", "Generated site directory") do |value|
    options["destination"] = File.expand_path(value)
  end
end.parse!

site = Jekyll::Site.new(Jekyll.configuration(options))
site.process

puts "Built #{site.pages.size} pages and #{site.posts.docs.size} posts into #{site.dest}"
