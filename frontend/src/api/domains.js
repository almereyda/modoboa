import repository from './repository'

const domainResource = 'domains'
const domainAliasResource = 'domainaliases'

export default {
  getDomains () {
    return repository.get(`/${domainResource}/`)
  },
  getDomain (domainId) {
    return repository.get(`/${domainResource}/${domainId}/`)
  },
  getDomainDNSDetail (domainId) {
    return repository.get(`/${domainResource}/${domainId}/dns_detail/`)
  },
  getDomainAliases (domain) {
    let url = `/${domainAliasResource}/`
    if (domain !== undefined) {
      url += `?domain=${domain}`
    }
    return repository.get(url)
  },
  createDomain (data) {
    return repository.post(`/${domainResource}/`, data)
  },
  updateDomain (domainId, data) {
    return repository.put(`/${domainResource}/${domainId}/`, data)
  },
  createDomainAlias (data) {
    return repository.post(`/${domainAliasResource}/`, data)
  },
  updateDomainAlias (aliasId, data) {
    return repository.put(`/${domainAliasResource}/${aliasId}/`, data)
  },
  deleteDomainAlias (aliasId) {
    return repository.delete(`/${domainAliasResource}/${aliasId}/`)
  }
}
