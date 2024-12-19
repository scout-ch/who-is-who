# frozen_string_literal: true

require "rails_helper"

RSpec.describe WidgetController, type: :request do
  let(:group_data) { build(:group_data) }
  let(:parent_group_data) { build(:group_data, id: group_data.links["parent"], name: "Parent Group") }
  let(:people_with_roles) { build(:people_with_roles) }

  let(:base_url) { "https://db.scout.ch/de/groups/" }
  let(:group_url) { "#{base_url}#{group_data.id}.json" }
  let(:parent_group_url) { "#{base_url}#{parent_group_data.id}.json" }
  let(:people_url) { "#{base_url}#{group_data.id}/people.json" }

  before do
    allow(ENV).to receive(:[]).and_call_original
    allow(ENV).to receive(:[]).with("INITIAL_GROUP_ID").and_return(group_data.id)

    stub_request(:get, group_url)
      .with(query: hash_including(token: ENV.fetch("HITOBITO_API_TOKEN", nil)))
      .to_return(status: 200, body: {
        "groups" => [{ "id" => group_data.id, "name" => group_data.name,
                       "links" => { "parent" => parent_group_data.id } }],
        "linked" => { "groups" => [parent_group_data.to_h] }
      }.to_json)

    stub_request(:get, parent_group_url)
      .with(query: hash_including(token: ENV.fetch("HITOBITO_API_TOKEN", nil)))
      .to_return(status: 200, body: {
        "groups" => [{ "id" => parent_group_data.id, "name" => parent_group_data.name }],
        "linked" => { "groups" => [] }
      }.to_json)

    stub_request(:get, people_url)
      .with(query: hash_including(token: ENV.fetch("HITOBITO_API_TOKEN", nil)))
      .to_return(status: 200, body: {
        "people" => people_with_roles.people.map(&:to_h),
        "linked" => { "roles" => people_with_roles.linked_roles.map(&:to_h) }
      }.to_json)
  end

  describe "GET #index" do
    context "when successfuly fetching" do
      before { get widget_index_path(group_id: group_data.id) }

      it "renders widget with correct group name and fetches group details successfully" do
        expect(response).to have_http_status(:ok)
        expect(response.body).to include("grid-widget", "AKom")
        expect(controller.instance_variable_get(:@group)).not_to be_nil

        sorted_people = controller.instance_variable_get(:@people)
        expect(sorted_people.map { |person| person["links"]["roles"].first }).to eq(%w[1 1 2])
      end
    end

    context "when fetching people details fails" do
      before do
        stub_request(:get,
                     people_url).with(query: hash_including(token: ENV.fetch("HITOBITO_API_TOKEN",
                                                                             nil))).to_return(status: 500)
        get widget_index_path(group_id: group_data.id)
      end

      it "renders error message" do
        expect(response).to have_http_status(:internal_server_error)
        expect(response.body).to include("Unable to fetch people at the moment. Please try again later.")
      end
    end

    context "when fetch_group_details receives a non-200 HTTP response" do
      before do
        stub_request(:get,
                     group_url).with(query: hash_including(token: ENV.fetch("HITOBITO_API_TOKEN",
                                                                            nil))).to_return(status: 500)
        get widget_index_path(group_id: group_data.id)
      end

      it "returns nil for group and parent_group and empty array for children_groups" do
        expect(controller.instance_variable_get(:@group)).to be_nil
        expect(controller.instance_variable_get(:@parent_group)).to be_nil
        expect(controller.instance_variable_get(:@children_groups)).to eq([])
      end
    end
  end

  describe "#fetch_group_details" do
    it "calls find_parent_group when group_id differs from initial_group_id" do
      allow(ENV).to receive(:[]).with("INITIAL_GROUP_ID").and_return("different_initial_group_id")
      widget_controller = described_class.new
      widget_controller.instance_variable_set(:@base_url, base_url)
      _, parent_group, = widget_controller.send(:fetch_group_details, group_data.id)
      expect(parent_group).not_to be_nil
      expect(parent_group["id"]).to eq(parent_group_data.id)
    end

    it "returns nil for group and parent_group and empty array for children_groups when response is nil" do
      allow(ENV).to receive(:[]).with("INITIAL_GROUP_ID").and_return(group_data.id)
      widget_controller = described_class.new
      widget_controller.instance_variable_set(:@base_url, base_url)

      allow(widget_controller).to receive(:fetch_data).and_return(nil)

      group, parent_group, children_groups = widget_controller.send(:fetch_group_details, group_data.id)
      expect(group).to be_nil
      expect(parent_group).to be_nil
      expect(children_groups).to eq([])
    end
  end

  describe "#fetch_initial_group_name" do
    it "returns nil when response is nil" do
      widget_controller = described_class.new
      widget_controller.instance_variable_set(:@base_url, base_url)

      allow(widget_controller).to receive(:fetch_data).and_return(nil)

      group_name = widget_controller.send(:fetch_initial_group_name, group_data.id)
      expect(group_name).to be_nil
    end
  end

  describe "#fetch_people_details" do
    it "returns nil for people and linked roles when response is nil" do
      widget_controller = described_class.new
      widget_controller.instance_variable_set(:@base_url, base_url)

      allow(widget_controller).to receive(:fetch_data).and_return(nil)

      people, linked_roles = widget_controller.send(:fetch_people_details, group_data.id)
      expect(people).to be_nil
      expect(linked_roles).to be_nil
    end
  end
end
