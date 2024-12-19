# frozen_string_literal: true

Struct.new("GroupData", :id, :type, :href, :group_type, :layer, :name, :short_name, :email, :links, :pbs_shortname,
           :website, :bank_account, :description, :created_at, :updated_at, :deleted_at, :available_roles)

FactoryBot.define do
  factory :group_data, class: "Struct::GroupData" do
    id { "9292" }
    type { "groups" }
    href { "https://db.scout.ch/de/groups/9292.json" }
    group_type { "Kommission" }
    layer { false }
    name { "AKom / CoFor / CommForm" }
    short_name { "" }
    email { nil }
    links do
      {
        "contact" => "13400",
        "creator" => "94518",
        "updater" => "29743",
        "parent" => "9288",
        "layer_group" => "2",
        "hierarchies" => %w[11747 2 9288 9292],
        "children" => %w[9293 9294]
      }
    end
    pbs_shortname { "AKom" }
    website { "" }
    bank_account { "" }
    description { "Ausbildungskommission / Commission formation / Commissione della formazione / Education commission" }
    created_at { "2019-09-10T15:25:17.000+02:00" }
    updated_at { "2024-10-08T08:06:14.000+02:00" }
    deleted_at { nil }
    available_roles do
      [
        { name: "Leiter*in", role_class: "Group::BundesKommission::Leitung" },
        { name: "Mitglied", role_class: "Group::BundesKommission::Mitglied" }
      ]
    end

    initialize_with { new(*attributes.values) }
  end

  factory :parent_group_data, class: "Struct::GroupData" do
    id { "9288" }
    type { "groups" }
    href { "https://db.scout.ch/de/groups/9288.json" }
    group_type { "Kommission" }
    layer { false }
    name { "Parent Group" }
    short_name { "" }
    email { nil }
    links { {} }
    pbs_shortname { "Parent" }
    website { "" }
    bank_account { "" }
    description { "Parent group description" }
    created_at { "2019-09-10T15:25:17.000+02:00" }
    updated_at { "2024-10-08T08:06:14.000+02:00" }
    deleted_at { nil }
    available_roles { [] }

    initialize_with { new(*attributes.values) }
  end
end
