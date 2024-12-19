# frozen_string_literal: true

class WidgetController < ApplicationController
  include WidgetHelper

  NATIONAL_ASSOCIATIONS = ["Kantonalverband", "Association cantonale", "associazione cantonale"].freeze

  before_action :set_language_and_base_url
  before_action :fetch_group_and_people_details

  def index; end

  private

  def fetch_group_and_people_details
    @initial_group_id = ENV["INITIAL_GROUP_ID"] || "2"
    @initial_group_name = fetch_initial_group_name(@initial_group_id)
    group_id = params["group_id"] || @initial_group_id
    @group, @parent_group, @children_groups = fetch_group_details(group_id)
    unless @group
      return render plain: "Unable to fetch group details at the moment. Please try again later.",
                    status: :service_unavailable
    end

    @people, @linked_roles = fetch_people_details(group_id)
    return if @people

    render plain: "Unable to fetch people at the moment. Please try again later.",
           status: :internal_server_error
  end

  def fetch_group_details(group_id)
    response = fetch_data("#{@base_url}#{group_id}.json")
    return [nil, nil, []] unless response&.code == 200

    group_details = JSON.parse(response.body)
    group = group_details["groups"].first
    parent_group = group_id == @initial_group_id ? nil : find_parent_group(group_details, group)
    children_groups = find_children_groups(group_details, group)
    [group, parent_group, children_groups]
  end

  def fetch_people_details(group_id)
    response = fetch_data("#{@base_url}#{group_id}/people.json", filter: "layer")
    return [nil, nil] unless response&.code == 200

    people_details = JSON.parse(response.body)
    people = people_details["people"] || []
    linked_roles = people_details.dig("linked", "roles") || []
    [sort_people_by_role(people, linked_roles), linked_roles]
  end

  def sort_people_by_role(people, linked_roles)
    role_priority = { "Leiter*in" => 1, "Mitglied" => 3 }
    default_priority = 2

    people.sort_by do |person|
      roles = person.dig("links", "roles").map { |role_id| find_role(role_id, linked_roles) }
      roles.map { |role| role_priority[role["role_type"]] || default_priority }.min
    end
  end

  def fetch_data(url, query_params = {})
    HTTParty.get(url, query: query_params.merge(token: ENV.fetch("HITOBITO_API_TOKEN", nil)))
  end

  def find_parent_group(group_details, group)
    group_details["linked"]["groups"].find { |current_group| current_group["id"] == group["links"]["parent"] }
  end

  def find_children_groups(group_details, parent_group)
    parent_group_children = parent_group["links"]["children"] || []
    group_details["linked"]["groups"].select do |current_group|
      parent_group_children.include?(current_group["id"]) &&
        NATIONAL_ASSOCIATIONS.exclude?(current_group["group_type"]) &&
        current_group["name"] != "Weitere"
    end
  end

  def set_language_and_base_url
    @language = params[:lang] || "de"
    @base_url = "https://db.scout.ch/#{@language}/groups/"
  end

  def fetch_initial_group_name(group_id)
    response = fetch_data("#{@base_url}#{group_id}.json")
    return nil unless response&.code == 200

    group_details = JSON.parse(response.body)
    group_details.dig("groups", 0, "name")
  end
end
