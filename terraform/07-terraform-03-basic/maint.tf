provider "yandex" {
  service_account_key_file = "key.json"
  cloud_id                 = var.yc_cloud_id
  folder_id                = var.yc_folder_id
  zone                     = var.yc_region
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2004-lts"
}

locals {
  instance_count = {
    stage = 1
    prod = 2
  }
  vm-name = toset(["vm-0", "vm-1"])
}

resource "yandex_vpc_network" "net" {
  name = "net"
  folder_id = var.yc_folder_id
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "subnet"
  network_id     = resource.yandex_vpc_network.net.id
  v4_cidr_blocks = ["10.2.0.0/16"]
  zone           = var.yc_region
}

resource "yandex_compute_instance" "vm-id" {
    lifecycle {
    create_before_destroy = true
    }
      name        = "vm-ubuntu-${count.index}-${terraform.workspace}"
      hostname    = "netology-tf-${count.index}-${terraform.workspace}.local"
      platform_id = "standard-v1"
      count = local.instance_count[terraform.workspace]

      resources {
        cores         = 2
        memory        = 2
        core_fraction = 100
      }

      boot_disk {
        initialize_params {
          image_id = data.yandex_compute_image.ubuntu.id
          type     = "network-hdd"
          size     = "20"
        }
      }

      network_interface {
        subnet_id = yandex_vpc_subnet.subnet.id
        nat       = true
        ipv6      = false
      }

      metadata = {
        ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
      }
}
resource "yandex_compute_instance" "vm-id2" {
    lifecycle {
    create_before_destroy = true
    }
    for_each = local.vm-name

      name        = each.value
      hostname    = "${each.value}.local"
      platform_id = "standard-v1"

      resources {
        cores         = 2
        memory        = 2
        core_fraction = 100
      }

      boot_disk {
        initialize_params {
          image_id = data.yandex_compute_image.ubuntu.id
          type     = "network-hdd"
          size     = "20"
        }
      }

      network_interface {
        subnet_id = yandex_vpc_subnet.subnet.id
        nat       = true
        ipv6      = false
      }

      metadata = {
        ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
      }
}