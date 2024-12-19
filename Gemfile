# frozen_string_literal: true

source "https://rubygems.org"

ruby "3.3.4"

gem "rails", "~> 7.1.3", ">= 7.1.3.4"

gem "bootsnap", require: false
gem "bootstrap"
gem "dartsass-sprockets"
gem "httparty"
gem "importmap-rails"
gem "jbuilder"
gem "pg"
gem "puma", ">= 5.0"
gem "redis", ">= 4.0.1"
gem "sprockets-rails"
gem "stimulus-rails"
gem "turbo-rails"
gem "tzinfo-data", platforms: %i[windows jruby]

group :development, :test do
  gem "brakeman", require: false
  gem "debug", platforms: %i[mri windows]
  gem "dotenv"
  gem "erb_lint", require: false
  gem "factory_bot_rails"
  gem "renuocop", require: false
  gem "rspec-rails"
end

group :development do
  gem "web-console"
end

group :test do
  gem "capybara"
  gem "rspec"
  gem "selenium-webdriver"
  gem "shoulda-matchers"
  gem "simplecov", require: false
  gem "super_diff"
  gem "webmock"
end
