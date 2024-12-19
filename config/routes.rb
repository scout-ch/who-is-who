# frozen_string_literal: true

Rails.application.routes.draw do
  root "widget#index"

  get "widget/index"
  get "up", to: "rails/health#show", as: :rails_health_check
end
