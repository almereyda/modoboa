<template>
<creation-form
  ref="form"
  :title="'New account'|translate"
  :steps="steps"
  :form-getter="getForm"
  :form-observer-getter="getObserver"
  :validate-object="validateAccount"
  :summary-sections="summarySections"
  @close="close"
  @create="submit"
  >
  <template v-slot:form.role="{ step }">
    <account-role-form :ref="`form_${step}`" v-model="account.role" :account="account" />
  </template>
  <template v-slot:form.identification="{ step }">
    <account-general-form v-if="step >= 2" :ref="`form_${step}`" v-model="account" />
  </template>
  <template v-slot:form.mailbox="{ step }">
    <account-mailbox-form :ref="`form_${step}`" v-model="account" />
  </template>
  <template v-slot:form.aliases="{ step }">
    <account-alias-form v-if="step >= 4" :ref="`form_${step}`" v-model="account" />
  </template>
  <template v-slot:item.random_password="{ item }">
    <template v-if="item.value">
      <v-col cols="12" class="highligth white--text">
        <v-row>
          <v-col><span>{{ item.key }}</span></v-col>
          <v-col class="text-right" v-if="item.type === 'yesno'">
            {{ item.value|yesno }}
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-right py-1">
            {{ account.password }}
            <v-btn icon color="white" :title="'Copy to clipboard'|translate" @click="copyPassword">
              <v-icon>mdi-clipboard-multiple-outline</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </template>
    <template v-else>
      <v-col><span class="grey--text">{{ item.key }}</span></v-col>
      <v-col class="text-right" v-if="item.type === 'yesno'">{{ item.value|yesno }}</v-col>
    </template>
  </template>
</creation-form>
</template>

<script>
import { mapGetters } from 'vuex'
import { bus } from '@/main'
import accounts from '@/api/accounts'
import AccountAliasForm from './AccountAliasForm'
import AccountGeneralForm from './AccountGeneralForm'
import AccountMailboxForm from './AccountMailboxForm'
import AccountRoleForm from './AccountRoleForm'
import CreationForm from '@/components/tools/CreationForm'

export default {
  components: {
    AccountAliasForm,
    AccountGeneralForm,
    AccountMailboxForm,
    AccountRoleForm,
    CreationForm
  },
  computed: {
    needsMailbox () {
      return this.account.role !== 'SuperAdmins' || (this.account.username && this.account.username.indexOf('@') !== -1)
    },
    ...mapGetters({
      authUser: 'auth/authUser'
    }),
    summarySections () {
      const result = [
        {
          title: this.$gettext('Role'),
          items: [
            { key: this.$gettext('Role'), value: this.account.role }
          ]
        },
        {
          title: this.$gettext('Identification'),
          items: [
            { key: this.$gettext('Username'), value: this.account.username },
            { key: this.$gettext('First name'), value: this.account.first_name },
            { key: this.$gettext('Last name'), value: this.account.last_name },
            {
              name: 'random_password',
              key: this.$gettext('Random password'),
              value: this.account.random_password,
              type: 'yesno'
            },
            {
              key: this.$gettext('Enabled'),
              value: this.account.is_active,
              type: 'yesno'
            }
          ]
        }
      ]
      if (this.needsMailbox) {
        return result.concat([
          {
            title: this.$gettext('Mailbox'),
            items: [
              { key: this.$gettext('Email'), value: this.account.mailbox.full_address },
              {
                key: this.$gettext('Quota'),
                value: (this.account.mailbox.use_domain_quota)
                  ? this.$gettext('Domain default value')
                  : this.account.mailbox.quota
              },
              {
                key: this.$gettext('Message sending limit'),
                value: this.account.mailbox.message_limit
              },
              {
                key: this.$gettext('Send only account'),
                value: this.account.mailbox.is_send_only,
                type: 'yesno'
              }
            ]
          },
          {
            title: this.$gettext('Aliases'),
            items: [
              {
                key: this.$gettext('Aliases'),
                value: this.account.aliases,
                type: 'list'
              }
            ]
          }
        ])
      }
      return result
    },
    steps () {
      const result = [
        {
          name: 'role',
          title: this.$gettext('Role')
        },
        {
          name: 'identification',
          title: this.$gettext('Identification')
        }
      ]
      if (this.needsMailbox) {
        return result.concat([
          {
            name: 'mailbox',
            title: this.$gettext('Mailbox')
          },
          {
            name: 'aliases',
            title: this.$gettext('Aliases')
          }
        ])
      }
      return result
    }
  },
  data () {
    return {
      account: this.getInitialForm()
    }
  },
  methods: {
    copyPassword () {
      navigator.clipboard.writeText(this.account.password).then(() => {
        bus.$emit('notification', { msg: this.$gettext('Password copied to clipboard') })
      })
    },
    getInitialForm () {
      return {
        aliases: [],
        is_active: true,
        role: 'SimpleUsers',
        mailbox: {
          use_domain_quota: true
        },
        random_password: true
      }
    },
    getForm (step) {
      return this.$refs[`form_${step}`]
    },
    getObserver (step) {
      return this.$refs[`form_${step}`].$refs.observer
    },
    preparePayload (payload) {
      if (payload.role === 'SuperAdmins' && payload.username && payload.username.indexOf('@') === -1) {
        delete payload.mailbox
      }
      if (payload.mailbox && payload.mailbox.message_limit === '') {
        this.$set(payload.mailbox, 'message_limit', undefined)
      }
    },
    validateAccount () {
      const payload = { ...this.account }
      this.preparePayload(payload)
      return accounts.validate(payload)
    },
    close () {
      this.account = this.getInitialForm()
      this.$refs.form.resetForm()
      this.$emit('close')
    },
    submit () {
      const data = { ...this.account }
      this.preparePayload(data)
      accounts.create(data).then(() => {
        bus.$emit('notification', { msg: this.$gettext('Account created') })
        this.$emit('created')
        this.close()
      })
    }
  },
  mounted () {
    this.$store.dispatch('identities/fetchDomains')
  },
  watch: {
    'account.role' () {
      delete this.account.username
    }
  }
}
</script>

<style lang="scss">
.highligth {
  background-color: #515D78;
}
</style>
